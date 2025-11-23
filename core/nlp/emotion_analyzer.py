"""
Emotion analysis module for WhisPay.
Detects emotions and confidence levels from speech tone and text.
"""

import numpy as np
import librosa
from typing import Dict, Optional, Tuple
from utils.logger import log
from app.config import settings


class EmotionAnalyzer:
    """Analyzes emotion and confidence from voice and text."""
    
    # Emotional keywords for text-based analysis
    EMOTION_KEYWORDS = {
        'confident': ['sure', 'definitely', 'absolutely', 'yes', 'correct', 'right'],
        'uncertain': ['maybe', 'perhaps', 'unsure', 'think', 'guess', 'not sure', 'um', 'uh'],
        'stressed': ['worried', 'concerned', 'anxious', 'nervous', 'scared', 'afraid'],
        'happy': ['great', 'good', 'excellent', 'wonderful', 'fantastic', 'thanks'],
        'angry': ['frustrated', 'angry', 'annoyed', 'upset', 'mad'],
        'confused': ['confused', 'don\'t understand', 'what', 'how', 'unclear']
    }
    
    def __init__(self):
        """Initialize the emotion analyzer."""
        log.info("Emotion analyzer initialized")
    
    def analyze_text(self, text: str) -> Dict[str, any]:
        """
        Analyze emotion from text content.
        
        Args:
            text: User input text
            
        Returns:
            Dictionary with detected emotions and scores
        """
        text_lower = text.lower()
        
        # Score each emotion
        emotion_scores = {}
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Detect uncertainty markers
        uncertainty_markers = ['um', 'uh', 'er', 'hmm', '...', 'maybe']
        uncertainty_count = sum(1 for marker in uncertainty_markers if marker in text_lower)
        
        # Determine primary emotion
        primary_emotion = 'neutral'
        if emotion_scores:
            primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        
        result = {
            'primary_emotion': primary_emotion,
            'emotion_scores': emotion_scores,
            'uncertainty_level': min(uncertainty_count / 3.0, 1.0),
            'is_uncertain': uncertainty_count >= 2
        }
        
        log.info(f"Text emotion analysis: {primary_emotion} (uncertainty: {result['uncertainty_level']:.2f})")
        return result
    
    def analyze_audio(self, audio_data: np.ndarray, sample_rate: int = None) -> Dict[str, any]:
        """
        Analyze emotion from audio features.
        
        Args:
            audio_data: Raw audio data
            sample_rate: Audio sample rate
            
        Returns:
            Dictionary with audio-based emotion indicators
        """
        sample_rate = sample_rate or settings.voice_sample_rate
        
        try:
            # Extract audio features
            features = self._extract_prosodic_features(audio_data, sample_rate)
            
            # Analyze confidence based on voice characteristics
            confidence = self._estimate_confidence(features)
            stress_level = self._estimate_stress(features)
            
            result = {
                'confidence_level': confidence,
                'stress_level': stress_level,
                'is_stressed': stress_level > 0.6,
                'is_hesitant': confidence < 0.4,
                'speaking_rate': features.get('speaking_rate', 0),
                'pitch_variance': features.get('pitch_variance', 0)
            }
            
            log.info(f"Audio emotion analysis - Confidence: {confidence:.2f}, Stress: {stress_level:.2f}")
            return result
            
        except Exception as e:
            log.error(f"Error analyzing audio emotion: {e}")
            return {
                'confidence_level': 0.5,
                'stress_level': 0.0,
                'is_stressed': False,
                'is_hesitant': False
            }
    
    def _extract_prosodic_features(self, audio_data: np.ndarray, sample_rate: int) -> Dict[str, float]:
        """
        Extract prosodic features from audio.
        
        Args:
            audio_data: Audio signal
            sample_rate: Sample rate
            
        Returns:
            Dictionary of prosodic features
        """
        try:
            # Pitch (F0) estimation
            pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sample_rate)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            # Energy/amplitude
            rms = librosa.feature.rms(y=audio_data)[0]
            
            # Zero crossing rate (indicates unvoiced segments)
            zcr = librosa.feature.zero_crossing_rate(audio_data)[0]
            
            # Speaking rate (approximate)
            onset_env = librosa.onset.onset_strength(y=audio_data, sr=sample_rate)
            tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sample_rate)[0]
            
            features = {
                'pitch_mean': float(np.mean(pitch_values)) if pitch_values else 0.0,
                'pitch_std': float(np.std(pitch_values)) if pitch_values else 0.0,
                'pitch_variance': float(np.var(pitch_values)) if pitch_values else 0.0,
                'energy_mean': float(np.mean(rms)),
                'energy_std': float(np.std(rms)),
                'zcr_mean': float(np.mean(zcr)),
                'speaking_rate': float(tempo) / 100.0  # Normalize
            }
            
            return features
            
        except Exception as e:
            log.error(f"Error extracting prosodic features: {e}")
            return {}
    
    def _estimate_confidence(self, features: Dict[str, float]) -> float:
        """
        Estimate speaker confidence from prosodic features.
        
        Args:
            features: Prosodic features
            
        Returns:
            Confidence score (0-1)
        """
        if not features:
            return 0.5
        
        # Confident speech typically has:
        # - Moderate pitch variance (not too monotone, not too erratic)
        # - Steady energy
        # - Moderate speaking rate
        
        confidence_score = 0.5
        
        # Pitch variance indicator
        pitch_var = features.get('pitch_variance', 0)
        if 500 < pitch_var < 3000:  # Optimal range
            confidence_score += 0.2
        
        # Energy stability
        energy_std = features.get('energy_std', 0)
        if energy_std < 0.1:  # Steady voice
            confidence_score += 0.2
        
        # Speaking rate
        speaking_rate = features.get('speaking_rate', 0)
        if 0.8 < speaking_rate < 1.5:  # Normal pace
            confidence_score += 0.1
        
        return min(confidence_score, 1.0)
    
    def _estimate_stress(self, features: Dict[str, float]) -> float:
        """
        Estimate stress level from prosodic features.
        
        Args:
            features: Prosodic features
            
        Returns:
            Stress score (0-1)
        """
        if not features:
            return 0.0
        
        # Stressed speech typically has:
        # - Higher pitch
        # - High pitch variance
        # - Faster speaking rate
        # - Higher energy variance
        
        stress_score = 0.0
        
        # High pitch indicator
        pitch_mean = features.get('pitch_mean', 0)
        if pitch_mean > 200:  # Higher than normal
            stress_score += 0.3
        
        # High pitch variance (erratic)
        pitch_var = features.get('pitch_variance', 0)
        if pitch_var > 3000:
            stress_score += 0.3
        
        # Fast speaking rate
        speaking_rate = features.get('speaking_rate', 0)
        if speaking_rate > 1.5:
            stress_score += 0.2
        
        # High energy variance
        energy_std = features.get('energy_std', 0)
        if energy_std > 0.15:
            stress_score += 0.2
        
        return min(stress_score, 1.0)
    
    def combined_analysis(
        self,
        text: str,
        audio_data: Optional[np.ndarray] = None,
        sample_rate: int = None
    ) -> Dict[str, any]:
        """
        Perform combined text and audio emotion analysis.
        
        Args:
            text: User input text
            audio_data: Audio data (optional)
            sample_rate: Sample rate for audio
            
        Returns:
            Combined emotion analysis results
        """
        # Text analysis
        text_result = self.analyze_text(text)
        
        # Audio analysis if available
        audio_result = {}
        if audio_data is not None:
            audio_result = self.analyze_audio(audio_data, sample_rate)
        
        # Combine results
        combined = {
            'text_emotion': text_result,
            'audio_emotion': audio_result,
            'overall_confidence': (
                text_result.get('uncertainty_level', 0.5) * 0.3 +
                audio_result.get('confidence_level', 0.5) * 0.7
            ) if audio_result else 1.0 - text_result.get('uncertainty_level', 0.5),
            'needs_reassurance': (
                text_result.get('is_uncertain', False) or
                audio_result.get('is_hesitant', False) or
                audio_result.get('is_stressed', False)
            )
        }
        
        return combined
