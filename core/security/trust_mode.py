"""
Adaptive trust mode for WhisPay.
Adjusts security requirements based on environmental factors.
"""

from typing import Dict, Optional
from enum import Enum
from utils.logger import log
from app.config import settings


class TrustLevel(Enum):
    """Trust level enumeration."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    CRITICAL = "critical"


class AdaptiveTrustMode:
    """Manages adaptive trust and security levels."""
    
    def __init__(self):
        """Initialize adaptive trust mode."""
        self.current_trust_level = TrustLevel.MEDIUM
        log.info("Adaptive trust mode initialized")
    
    def assess_trust_level(
        self,
        noise_level: float,
        voice_confidence: float,
        transaction_amount: Optional[float] = None,
        location_risk: Optional[str] = None
    ) -> TrustLevel:
        """
        Assess current trust level based on multiple factors.
        
        Args:
            noise_level: Background noise level (0-1)
            voice_confidence: Voice biometric confidence (0-1)
            transaction_amount: Transaction amount if applicable
            location_risk: Location risk assessment
            
        Returns:
            Assessed trust level
        """
        trust_score = 1.0
        
        # Factor 1: Environmental noise
        if noise_level > settings.background_noise_threshold:
            trust_score -= 0.3
            log.warning(f"High noise level detected: {noise_level:.2f}")
        
        # Factor 2: Voice biometric confidence
        if voice_confidence < settings.voice_biometric_threshold:
            trust_score -= 0.3
            log.warning(f"Low voice confidence: {voice_confidence:.2f}")
        
        # Factor 3: Transaction amount
        if transaction_amount:
            if transaction_amount > settings.high_value_threshold:
                trust_score -= 0.2
                log.info(f"High-value transaction detected: ₹{transaction_amount}")
        
        # Factor 4: Location risk
        if location_risk == "high":
            trust_score -= 0.2
            log.warning("High-risk location detected")
        
        # Determine trust level
        if trust_score >= 0.8:
            level = TrustLevel.HIGH
        elif trust_score >= 0.5:
            level = TrustLevel.MEDIUM
        elif trust_score >= 0.3:
            level = TrustLevel.LOW
        else:
            level = TrustLevel.CRITICAL
        
        self.current_trust_level = level
        log.info(f"Trust level assessed: {level.value} (score: {trust_score:.2f})")
        
        return level
    
    def get_required_authentication(self, trust_level: TrustLevel) -> Dict[str, bool]:
        """
        Get required authentication factors for trust level.
        
        Args:
            trust_level: Current trust level
            
        Returns:
            Dictionary of required authentication factors
        """
        requirements = {
            TrustLevel.HIGH: {
                'voice_biometric': True,
                'pin': False,
                'otp': False,
                'allow_sensitive_operations': True
            },
            TrustLevel.MEDIUM: {
                'voice_biometric': True,
                'pin': False,
                'otp': False,
                'allow_sensitive_operations': True
            },
            TrustLevel.LOW: {
                'voice_biometric': True,
                'pin': True,
                'otp': False,
                'allow_sensitive_operations': False
            },
            TrustLevel.CRITICAL: {
                'voice_biometric': True,
                'pin': True,
                'otp': True,
                'allow_sensitive_operations': False
            }
        }
        
        return requirements.get(trust_level, requirements[TrustLevel.CRITICAL])
    
    def should_switch_to_private_mode(self, trust_level: TrustLevel) -> bool:
        """
        Determine if private mode should be activated.
        
        Args:
            trust_level: Current trust level
            
        Returns:
            True if private mode recommended
        """
        return trust_level in [TrustLevel.LOW, TrustLevel.CRITICAL]
    
    def get_allowed_operations(self, trust_level: TrustLevel) -> Dict[str, bool]:
        """
        Get allowed operations for trust level.
        
        Args:
            trust_level: Current trust level
            
        Returns:
            Dictionary of allowed operations
        """
        operations = {
            TrustLevel.HIGH: {
                'check_balance': True,
                'transfer_money': True,
                'view_history': True,
                'apply_for_loan': True,
                'set_reminder': True,
                'max_transaction_amount': float('inf')
            },
            TrustLevel.MEDIUM: {
                'check_balance': True,
                'transfer_money': True,
                'view_history': True,
                'apply_for_loan': True,
                'set_reminder': True,
                'max_transaction_amount': settings.high_value_threshold
            },
            TrustLevel.LOW: {
                'check_balance': True,
                'transfer_money': True,
                'view_history': True,
                'apply_for_loan': False,
                'set_reminder': True,
                'max_transaction_amount': settings.default_transaction_limit
            },
            TrustLevel.CRITICAL: {
                'check_balance': True,
                'transfer_money': False,
                'view_history': True,
                'apply_for_loan': False,
                'set_reminder': False,
                'max_transaction_amount': 0
            }
        }
        
        return operations.get(trust_level, operations[TrustLevel.CRITICAL])
    
    def generate_trust_message(self, trust_level: TrustLevel, reason: str = "") -> str:
        """
        Generate user-friendly message about trust level.
        
        Args:
            trust_level: Current trust level
            reason: Reason for trust level change
            
        Returns:
            User message
        """
        messages = {
            TrustLevel.HIGH: "Everything looks secure. I'm ready to help you.",
            
            TrustLevel.MEDIUM: "I've verified your identity. How can I assist you?",
            
            TrustLevel.LOW: (
                f"I detected some environmental factors that affect security. "
                f"For your protection, I'll need additional verification for sensitive operations."
            ),
            
            TrustLevel.CRITICAL: (
                f"I detected background noise and can't verify your voice clearly. "
                f"For your security, let's switch to PIN verification for transactions."
            )
        }
        
        message = messages.get(trust_level, messages[TrustLevel.CRITICAL])
        
        if reason:
            message += f" {reason}"
        
        return message
    
    def requires_reverification(
        self,
        trust_level: TrustLevel,
        operation: str,
        amount: Optional[float] = None
    ) -> bool:
        """
        Check if operation requires additional verification.
        
        Args:
            trust_level: Current trust level
            operation: Operation to perform
            amount: Transaction amount if applicable
            
        Returns:
            True if reverification needed
        """
        # High-value transactions always need reverification
        if amount and amount > settings.require_reverification_above:
            return True
        
        # Check operation permissions
        allowed_ops = self.get_allowed_operations(trust_level)
        
        # If operation not allowed, reverification won't help
        if not allowed_ops.get(operation, False):
            return False
        
        # Low trust levels need reverification for sensitive ops
        sensitive_operations = ['transfer_money', 'apply_for_loan']
        if operation in sensitive_operations and trust_level in [TrustLevel.LOW, TrustLevel.CRITICAL]:
            return True
        
        return False
