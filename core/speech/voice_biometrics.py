"""
Voice biometrics module for WhisPay.
Provides voice-based user authentication using voice print matching.
"""

import numpy as np
import librosa
from typing import Optional, Dict, Tuple
import pickle
from pathlib import Path
from utils.logger import log
from utils.helpers import calculate_similarity, hash_voice_print
from app.config import settings


class VoiceBiometrics:
    """Handles voice biometric authentication."""
    
    def __init__(self, voice_prints_dir: str = "./data/users/voice_prints"):
        """
        Initialize voice biometrics system.
        
        Args:
            voice_prints_dir: Directory to store voice prints
        """
        self.voice_prints_dir = Path(voice_prints_dir)
        self.voice_prints_dir.mkdir(parents=True, exist_ok=True)
        self.threshold = settings.voice_biometric_threshold
        log.info("Voice biometrics system initialized")
    
    def extract_features(self, audio_data: np.ndarray, sample_rate: int = None) -> Optional[np.ndarray]:
        """
        Extract voice features (MFCC) from audio data.
        
        Args:
            audio_data: Raw audio data
            sample_rate: Audio sample rate
            
        Returns:
            Feature vector or None if extraction fails
        """
        sample_rate = sample_rate or settings.voice_sample_rate
        
        try:
            # Extract MFCC features (Mel-frequency cepstral coefficients)
            mfccs = librosa.feature.mfcc(
                y=audio_data,
                sr=sample_rate,
                n_mfcc=13
            )
            
            # Calculate delta and delta-delta features
            mfcc_delta = librosa.feature.delta(mfccs)
            mfcc_delta2 = librosa.feature.delta(mfccs, order=2)
            
            # Combine features
            features = np.concatenate([
                np.mean(mfccs, axis=1),
                np.std(mfccs, axis=1),
                np.mean(mfcc_delta, axis=1),
                np.mean(mfcc_delta2, axis=1)
            ])
            
            return features
            
        except Exception as e:
            log.error(f"Error extracting voice features: {e}")
            return None
    
    def enroll_user(self, user_id: str, audio_samples: list) -> bool:
        """
        Enroll a new user by creating voice print from multiple samples.
        
        Args:
            user_id: Unique user identifier
            audio_samples: List of audio data arrays for enrollment
            
        Returns:
            True if enrollment successful
        """
        if len(audio_samples) < 3:
            log.warning("At least 3 audio samples recommended for enrollment")
        
        try:
            # Extract features from each sample
            feature_vectors = []
            for audio in audio_samples:
                features = self.extract_features(audio)
                if features is not None:
                    feature_vectors.append(features)
            
            if len(feature_vectors) < 2:
                log.error("Not enough valid samples for enrollment")
                return False
            
            # Create voice print as average of feature vectors
            voice_print = np.mean(feature_vectors, axis=0)
            
            # Save voice print
            voice_print_path = self.voice_prints_dir / f"{user_id}.pkl"
            with open(voice_print_path, 'wb') as f:
                pickle.dump(voice_print, f)
            
            log.info(f"User {user_id} enrolled successfully")
            return True
            
        except Exception as e:
            log.error(f"Error enrolling user: {e}")
            return False
    
    def verify_user(self, user_id: str, audio_data: np.ndarray) -> Tuple[bool, float]:
        """
        Verify user identity using voice biometrics.
        
        Args:
            user_id: User identifier to verify against
            audio_data: Audio data to verify
            
        Returns:
            Tuple of (verification result, confidence score)
        """
        try:
            # Load stored voice print
            voice_print_path = self.voice_prints_dir / f"{user_id}.pkl"
            if not voice_print_path.exists():
                log.warning(f"No voice print found for user {user_id}")
                return False, 0.0
            
            with open(voice_print_path, 'rb') as f:
                stored_voice_print = pickle.load(f)
            
            # Extract features from current audio
            current_features = self.extract_features(audio_data)
            if current_features is None:
                log.error("Failed to extract features from audio")
                return False, 0.0
            
            # Calculate similarity
            similarity = calculate_similarity(
                stored_voice_print.tolist(),
                current_features.tolist()
            )
            
            # Verify against threshold
            verified = similarity >= self.threshold
            
            log.info(f"Voice verification for {user_id}: {verified} (score: {similarity:.3f})")
            return verified, similarity
            
        except Exception as e:
            log.error(f"Error verifying user: {e}")
            return False, 0.0
    
    def identify_user(self, audio_data: np.ndarray) -> Optional[Tuple[str, float]]:
        """
        Identify user from voice sample (1:N matching).
        
        Args:
            audio_data: Audio data to identify
            
        Returns:
            Tuple of (user_id, confidence) or None if no match
        """
        try:
            # Extract features from audio
            current_features = self.extract_features(audio_data)
            if current_features is None:
                return None
            
            # Compare against all enrolled users
            best_match = None
            best_score = 0.0
            
            for voice_print_file in self.voice_prints_dir.glob("*.pkl"):
                user_id = voice_print_file.stem
                
                with open(voice_print_file, 'rb') as f:
                    stored_voice_print = pickle.load(f)
                
                similarity = calculate_similarity(
                    stored_voice_print.tolist(),
                    current_features.tolist()
                )
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = user_id
            
            # Check if best match exceeds threshold
            if best_match and best_score >= self.threshold:
                log.info(f"User identified: {best_match} (score: {best_score:.3f})")
                return best_match, best_score
            
            log.info("No matching user found")
            return None
            
        except Exception as e:
            log.error(f"Error identifying user: {e}")
            return None
    
    def update_voice_print(self, user_id: str, audio_data: np.ndarray, weight: float = 0.1) -> bool:
        """
        Update existing voice print with new sample (adaptive learning).
        
        Args:
            user_id: User identifier
            audio_data: New audio sample
            weight: Weight for new sample (0.0 to 1.0)
            
        Returns:
            True if update successful
        """
        try:
            voice_print_path = self.voice_prints_dir / f"{user_id}.pkl"
            if not voice_print_path.exists():
                log.warning(f"No voice print found for user {user_id}")
                return False
            
            # Load existing voice print
            with open(voice_print_path, 'rb') as f:
                stored_voice_print = pickle.load(f)
            
            # Extract features from new sample
            new_features = self.extract_features(audio_data)
            if new_features is None:
                return False
            
            # Update voice print with weighted average
            updated_voice_print = (
                (1 - weight) * stored_voice_print +
                weight * new_features
            )
            
            # Save updated voice print
            with open(voice_print_path, 'wb') as f:
                pickle.dump(updated_voice_print, f)
            
            log.info(f"Voice print updated for user {user_id}")
            return True
            
        except Exception as e:
            log.error(f"Error updating voice print: {e}")
            return False
    
    def delete_voice_print(self, user_id: str) -> bool:
        """
        Delete user's voice print.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if deletion successful
        """
        try:
            voice_print_path = self.voice_prints_dir / f"{user_id}.pkl"
            if voice_print_path.exists():
                voice_print_path.unlink()
                log.info(f"Voice print deleted for user {user_id}")
                return True
            else:
                log.warning(f"No voice print found for user {user_id}")
                return False
                
        except Exception as e:
            log.error(f"Error deleting voice print: {e}")
            return False
