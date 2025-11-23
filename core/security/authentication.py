"""
Authentication manager for WhisPay.
Handles multi-factor authentication and session management.
"""

from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta
import secrets
import hashlib
from utils.logger import log
from app.config import settings


class AuthenticationManager:
    """Manages user authentication and sessions."""
    
    def __init__(self):
        """Initialize authentication manager."""
        self.sessions: Dict[str, Dict] = {}
        self.otp_store: Dict[str, Dict] = {}
        log.info("Authentication manager initialized")
    
    def generate_otp(self, user_id: str, length: int = 6) -> str:
        """
        Generate one-time password for user.
        
        Args:
            user_id: User identifier
            length: OTP length
            
        Returns:
            Generated OTP
        """
        otp = ''.join([str(secrets.randbelow(10)) for _ in range(length)])
        
        # Store OTP with expiration
        self.otp_store[user_id] = {
            'otp': otp,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(minutes=5),
            'attempts': 0
        }
        
        log.info(f"OTP generated for user {user_id}")
        return otp
    
    def verify_otp(self, user_id: str, otp: str) -> bool:
        """
        Verify OTP for user.
        
        Args:
            user_id: User identifier
            otp: OTP to verify
            
        Returns:
            True if OTP is valid
        """
        if user_id not in self.otp_store:
            log.warning(f"No OTP found for user {user_id}")
            return False
        
        stored_otp = self.otp_store[user_id]
        
        # Check expiration
        if datetime.now() > stored_otp['expires_at']:
            log.warning(f"OTP expired for user {user_id}")
            del self.otp_store[user_id]
            return False
        
        # Check attempts
        if stored_otp['attempts'] >= 3:
            log.warning(f"Too many OTP attempts for user {user_id}")
            del self.otp_store[user_id]
            return False
        
        # Verify OTP
        if otp == stored_otp['otp']:
            log.info(f"OTP verified for user {user_id}")
            del self.otp_store[user_id]
            return True
        else:
            stored_otp['attempts'] += 1
            log.warning(f"Invalid OTP for user {user_id} (attempt {stored_otp['attempts']})")
            return False
    
    def generate_pin_hash(self, pin: str) -> str:
        """
        Generate hash of PIN for storage.
        
        Args:
            pin: User PIN
            
        Returns:
            Hashed PIN
        """
        return hashlib.sha256(pin.encode()).hexdigest()
    
    def verify_pin(self, pin: str, pin_hash: str) -> bool:
        """
        Verify PIN against stored hash.
        
        Args:
            pin: PIN to verify
            pin_hash: Stored PIN hash
            
        Returns:
            True if PIN matches
        """
        computed_hash = self.generate_pin_hash(pin)
        return computed_hash == pin_hash
    
    def create_session(self, user_id: str, authentication_method: str) -> str:
        """
        Create authenticated session for user.
        
        Args:
            user_id: User identifier
            authentication_method: Method used (voice, pin, otp)
            
        Returns:
            Session token
        """
        session_token = secrets.token_urlsafe(32)
        
        self.sessions[session_token] = {
            'user_id': user_id,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(minutes=settings.jwt_expiration_minutes),
            'authentication_method': authentication_method,
            'is_active': True
        }
        
        log.info(f"Session created for user {user_id} via {authentication_method}")
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[str]:
        """
        Validate session token and return user ID.
        
        Args:
            session_token: Session token to validate
            
        Returns:
            User ID if session valid, None otherwise
        """
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        
        # Check expiration
        if datetime.now() > session['expires_at']:
            log.warning(f"Session expired for user {session['user_id']}")
            del self.sessions[session_token]
            return None
        
        # Check if active
        if not session['is_active']:
            log.warning(f"Inactive session for user {session['user_id']}")
            return None
        
        return session['user_id']
    
    def end_session(self, session_token: str) -> bool:
        """
        End user session.
        
        Args:
            session_token: Session token to end
            
        Returns:
            True if session ended successfully
        """
        if session_token in self.sessions:
            user_id = self.sessions[session_token]['user_id']
            del self.sessions[session_token]
            log.info(f"Session ended for user {user_id}")
            return True
        return False
    
    def extend_session(self, session_token: str, minutes: int = None) -> bool:
        """
        Extend session expiration.
        
        Args:
            session_token: Session token
            minutes: Minutes to extend (default from settings)
            
        Returns:
            True if extended successfully
        """
        if session_token not in self.sessions:
            return False
        
        minutes = minutes or settings.jwt_expiration_minutes
        self.sessions[session_token]['expires_at'] = datetime.now() + timedelta(minutes=minutes)
        
        log.info(f"Session extended for user {self.sessions[session_token]['user_id']}")
        return True
    
    def cleanup_expired_sessions(self):
        """Remove all expired sessions."""
        now = datetime.now()
        expired = [
            token for token, session in self.sessions.items()
            if now > session['expires_at']
        ]
        
        for token in expired:
            user_id = self.sessions[token]['user_id']
            del self.sessions[token]
            log.info(f"Removed expired session for user {user_id}")
        
        if expired:
            log.info(f"Cleaned up {len(expired)} expired sessions")
