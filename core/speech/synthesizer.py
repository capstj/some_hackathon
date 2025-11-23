"""
Text-to-speech synthesis module for WhisPay.
Converts text responses to natural-sounding speech.
"""

import pyttsx3
from typing import Optional
from utils.logger import log
from app.config import settings


class SpeechSynthesizer:
    """Handles text-to-speech conversion."""
    
    def __init__(self):
        """Initialize the speech synthesizer."""
        try:
            self.engine = pyttsx3.init()
            self._configure_engine()
            log.info("Speech synthesizer initialized")
        except Exception as e:
            log.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None
    
    def _configure_engine(self):
        """Configure TTS engine with settings."""
        if not self.engine:
            return
            
        # Set speech rate
        self.engine.setProperty('rate', settings.tts_rate)
        
        # Set volume
        self.engine.setProperty('volume', settings.tts_volume)
        
        # Set voice (male/female)
        voices = self.engine.getProperty('voices')
        if voices:
            # Try to find matching voice
            voice_preference = settings.tts_voice.lower()
            selected_voice = None
            
            for voice in voices:
                if voice_preference in voice.name.lower():
                    selected_voice = voice.id
                    break
            
            if not selected_voice and voices:
                # Fallback to first available voice
                selected_voice = voices[0].id
            
            if selected_voice:
                self.engine.setProperty('voice', selected_voice)
                log.info(f"Voice set to: {selected_voice}")
    
    def speak(self, text: str, block: bool = True) -> bool:
        """
        Convert text to speech and play it.
        
        Args:
            text: Text to speak
            block: Whether to wait for speech to complete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.engine:
            log.error("TTS engine not initialized")
            return False
        
        try:
            log.info(f"Speaking: {text}")
            self.engine.say(text)
            
            if block:
                self.engine.runAndWait()
            
            return True
            
        except Exception as e:
            log.error(f"Error during speech synthesis: {e}")
            return False
    
    def stop(self):
        """Stop current speech playback."""
        if self.engine:
            try:
                self.engine.stop()
            except Exception as e:
                log.error(f"Error stopping speech: {e}")
    
    def save_to_file(self, text: str, filename: str) -> bool:
        """
        Save synthesized speech to audio file.
        
        Args:
            text: Text to synthesize
            filename: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        if not self.engine:
            log.error("TTS engine not initialized")
            return False
        
        try:
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            log.info(f"Speech saved to: {filename}")
            return True
            
        except Exception as e:
            log.error(f"Error saving speech to file: {e}")
            return False
    
    def set_rate(self, rate: int):
        """
        Adjust speech rate.
        
        Args:
            rate: Words per minute (typically 100-200)
        """
        if self.engine:
            self.engine.setProperty('rate', rate)
            log.info(f"Speech rate set to: {rate}")
    
    def set_volume(self, volume: float):
        """
        Adjust speech volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if self.engine:
            volume = max(0.0, min(1.0, volume))  # Clamp to valid range
            self.engine.setProperty('volume', volume)
            log.info(f"Speech volume set to: {volume}")
