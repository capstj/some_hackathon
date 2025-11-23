"""
Speech recognition module for WhisPay.
Converts spoken audio to text using various speech recognition engines.
"""

import speech_recognition as sr
from typing import Optional, Dict, Any
import sounddevice as sd
import numpy as np
from utils.logger import log
from app.config import settings


class SpeechRecognizer:
    """Handles speech-to-text conversion."""
    
    def __init__(self):
        """Initialize the speech recognizer."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise on initialization
        with self.microphone as source:
            log.info("Calibrating for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            log.info("Calibration complete")
    
    def listen(self, timeout: Optional[int] = None, phrase_time_limit: Optional[int] = None) -> Optional[str]:
        """
        Listen for speech input and convert to text.
        
        Args:
            timeout: Maximum time to wait for speech to start (seconds)
            phrase_time_limit: Maximum time for phrase (seconds)
            
        Returns:
            Recognized text or None if recognition failed
        """
        timeout = timeout or settings.speech_timeout
        phrase_time_limit = phrase_time_limit or settings.speech_phrase_time_limit
        
        try:
            with self.microphone as source:
                log.info("Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
            log.info("Processing speech...")
            text = self._recognize_speech(audio)
            
            if text:
                log.info(f"Recognized: {text}")
                return text
            else:
                log.warning("Could not recognize speech")
                return None
                
        except sr.WaitTimeoutError:
            log.warning("Listening timed out - no speech detected")
            return None
        except Exception as e:
            log.error(f"Error during speech recognition: {e}")
            return None
    
    def _recognize_speech(self, audio: sr.AudioData) -> Optional[str]:
        """
        Recognize speech from audio data using configured engine.
        
        Args:
            audio: Audio data to recognize
            
        Returns:
            Recognized text or None
        """
        engine = settings.speech_recognition_engine.lower()
        language = settings.speech_language
        
        try:
            if engine == "google":
                return self.recognizer.recognize_google(audio, language=language)
            elif engine == "sphinx":
                return self.recognizer.recognize_sphinx(audio)
            elif engine == "wit":
                # Requires WIT_AI_KEY in settings
                return self.recognizer.recognize_wit(audio, key=settings.wit_ai_key)
            else:
                log.warning(f"Unknown engine '{engine}', falling back to Google")
                return self.recognizer.recognize_google(audio, language=language)
                
        except sr.UnknownValueError:
            log.warning("Speech was unintelligible")
            return None
        except sr.RequestError as e:
            log.error(f"Could not request results from speech recognition service: {e}")
            return None
        except Exception as e:
            log.error(f"Error recognizing speech: {e}")
            return None
    
    def get_audio_data(self, duration: int = 3) -> Optional[np.ndarray]:
        """
        Record raw audio data for voice biometrics.
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Raw audio data as numpy array or None
        """
        try:
            log.info(f"Recording {duration} seconds of audio...")
            audio_data = sd.rec(
                int(duration * settings.voice_sample_rate),
                samplerate=settings.voice_sample_rate,
                channels=settings.voice_channels,
                dtype=np.float32
            )
            sd.wait()
            log.info("Recording complete")
            return audio_data.flatten()
            
        except Exception as e:
            log.error(f"Error recording audio: {e}")
            return None
    
    def measure_background_noise(self, duration: float = 1.0) -> float:
        """
        Measure ambient background noise level.
        
        Args:
            duration: Duration to measure (seconds)
            
        Returns:
            Noise level (0.0 to 1.0)
        """
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
                
            # Calculate energy level as proxy for noise
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            energy = np.sqrt(np.mean(audio_data ** 2))
            
            # Normalize to 0-1 range (assuming max energy of 10000)
            noise_level = min(energy / 10000.0, 1.0)
            
            log.info(f"Background noise level: {noise_level:.2f}")
            return noise_level
            
        except Exception as e:
            log.error(f"Error measuring background noise: {e}")
            return 0.0
    
    def is_noisy_environment(self) -> bool:
        """
        Check if current environment is too noisy for reliable recognition.
        
        Returns:
            True if environment exceeds noise threshold
        """
        noise_level = self.measure_background_noise()
        return noise_level > settings.background_noise_threshold
