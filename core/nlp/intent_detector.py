"""
Intent detection module for WhisPay.
Classifies user utterances into banking intents.
"""

from typing import Dict, Optional, List
import re
from utils.logger import log
from utils.helpers import sanitize_input


class IntentDetector:
    """Detects user intent from natural language input."""
    
    # Intent patterns with keywords
    INTENT_PATTERNS = {
        'check_balance': [
            r'\b(balance|total|amount|money|funds?)\b',
            r'\b(how much|what\'?s my|check)\b',
            r'\b(account|saving|current)\b'
        ],
        'transfer_money': [
            r'\b(transfer|send|pay|give)\b',
            r'\b(to|for)\s+\w+',
            r'\b\d+\b.*\b(rupees?|rs\.?|inr|₹)\b'
        ],
        'transaction_history': [
            r'\b(history|transactions?|statement)\b',
            r'\b(show|view|get|see)\b',
            r'\b(recent|last|previous)\b'
        ],
        'loan_inquiry': [
            r'\b(loan|credit|borrow)\b',
            r'\b(apply|eligible|rate|emi)\b',
            r'\b(personal|home|car|education)\b'
        ],
        'set_reminder': [
            r'\b(remind|reminder|alert)\b',
            r'\b(set|create|add)\b',
            r'\b(payment|bill|due)\b'
        ],
        'monthly_summary': [
            r'\b(summary|report|spending)\b',
            r'\b(month|monthly)\b',
            r'\b(habit|pattern|analysis)\b'
        ],
        'confirm_action': [
            r'\b(yes|yeah|yep|confirm|proceed|ok|sure|correct)\b'
        ],
        'deny_action': [
            r'\b(no|nope|cancel|stop|don\'?t|never mind)\b'
        ],
        'help': [
            r'\b(help|what can you|capabilities|features)\b',
            r'\b(how to|how do i)\b'
        ],
        'greeting': [
            r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b'
        ],
        'thank_you': [
            r'\b(thank|thanks|appreciate)\b'
        ],
        'goodbye': [
            r'\b(bye|goodbye|see you|good night)\b'
        ]
    }
    
    def __init__(self):
        """Initialize the intent detector."""
        log.info("Intent detector initialized")
    
    def detect(self, text: str) -> Dict[str, any]:
        """
        Detect intent from user input.
        
        Args:
            text: User input text
            
        Returns:
            Dictionary with intent and confidence
        """
        text = sanitize_input(text.lower())
        
        # Score each intent
        intent_scores = {}
        for intent, patterns in self.INTENT_PATTERNS.items():
            score = self._score_intent(text, patterns)
            if score > 0:
                intent_scores[intent] = score
        
        # Get best matching intent
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            confidence = min(best_intent[1] / len(self.INTENT_PATTERNS[best_intent[0]]), 1.0)
            
            result = {
                'intent': best_intent[0],
                'confidence': confidence,
                'all_scores': intent_scores
            }
            
            log.info(f"Detected intent: {best_intent[0]} (confidence: {confidence:.2f})")
            return result
        
        # No clear intent detected
        log.warning(f"Could not determine intent for: {text}")
        return {
            'intent': 'unknown',
            'confidence': 0.0,
            'all_scores': {}
        }
    
    def _score_intent(self, text: str, patterns: List[str]) -> int:
        """
        Score how well text matches intent patterns.
        
        Args:
            text: Input text
            patterns: List of regex patterns for intent
            
        Returns:
            Match score
        """
        score = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 1
        return score
    
    def requires_confirmation(self, intent: str) -> bool:
        """
        Check if intent requires user confirmation.
        
        Args:
            intent: Detected intent
            
        Returns:
            True if confirmation needed
        """
        high_risk_intents = ['transfer_money', 'loan_inquiry', 'set_reminder']
        return intent in high_risk_intents
    
    def get_intent_description(self, intent: str) -> str:
        """
        Get human-readable description of intent.
        
        Args:
            intent: Intent name
            
        Returns:
            Description string
        """
        descriptions = {
            'check_balance': 'Check account balance',
            'transfer_money': 'Transfer funds',
            'transaction_history': 'View transaction history',
            'loan_inquiry': 'Inquire about loans',
            'set_reminder': 'Set payment reminder',
            'monthly_summary': 'Get monthly spending summary',
            'confirm_action': 'Confirm action',
            'deny_action': 'Cancel action',
            'help': 'Get help',
            'greeting': 'Greeting',
            'thank_you': 'Thank you',
            'goodbye': 'Goodbye',
            'unknown': 'Unknown intent'
        }
        return descriptions.get(intent, 'Unknown')
