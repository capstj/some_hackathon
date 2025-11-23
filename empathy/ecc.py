"""
Emotional Confidence Check (ECC) module for WhisPay.
Provides empathetic responses based on user's emotional state.
"""

from typing import Dict, Optional
from core.nlp.emotion_analyzer import EmotionAnalyzer
from utils.logger import log


class EmotionalConfidenceCheck:
    """Handles emotional confidence checks and empathetic responses."""
    
    def __init__(self):
        """Initialize ECC system."""
        self.emotion_analyzer = EmotionAnalyzer()
        log.info("Emotional Confidence Check initialized")
    
    def check_confidence(
        self,
        text: str,
        audio_data: Optional[any] = None,
        context: Optional[str] = None
    ) -> Dict:
        """
        Perform emotional confidence check.
        
        Args:
            text: User's text input
            audio_data: Audio data if available
            context: Current interaction context
            
        Returns:
            Dictionary with confidence assessment and response
        """
        # Analyze emotions
        emotion_result = self.emotion_analyzer.combined_analysis(text, audio_data)
        
        # Determine if reassurance needed
        needs_reassurance = emotion_result.get('needs_reassurance', False)
        overall_confidence = emotion_result.get('overall_confidence', 0.5)
        
        # Get text emotion details
        text_emotion = emotion_result.get('text_emotion', {})
        primary_emotion = text_emotion.get('primary_emotion', 'neutral')
        is_uncertain = text_emotion.get('is_uncertain', False)
        
        # Get audio emotion details
        audio_emotion = emotion_result.get('audio_emotion', {})
        is_stressed = audio_emotion.get('is_stressed', False)
        is_hesitant = audio_emotion.get('is_hesitant', False)
        
        result = {
            'needs_reassurance': needs_reassurance,
            'confidence_level': overall_confidence,
            'primary_emotion': primary_emotion,
            'is_uncertain': is_uncertain,
            'is_stressed': is_stressed,
            'is_hesitant': is_hesitant,
            'should_intervene': False,
            'response': None
        }
        
        # Generate appropriate response
        if needs_reassurance or overall_confidence < 0.4:
            result['should_intervene'] = True
            result['response'] = self._generate_reassurance_response(
                primary_emotion,
                is_uncertain,
                is_stressed,
                context
            )
        
        log.info(f"ECC: Confidence {overall_confidence:.2f}, Emotion: {primary_emotion}, Intervene: {result['should_intervene']}")
        return result
    
    def _generate_reassurance_response(
        self,
        emotion: str,
        is_uncertain: bool,
        is_stressed: bool,
        context: Optional[str] = None
    ) -> str:
        """
        Generate empathetic reassurance response.
        
        Args:
            emotion: Primary detected emotion
            is_uncertain: Whether user seems uncertain
            is_stressed: Whether user seems stressed
            context: Current context
            
        Returns:
            Reassurance message
        """
        responses = {
            'uncertain': [
                "You sound unsure. Would you like me to review the details before we proceed?",
                "I sense some hesitation. Let me walk you through this step by step.",
                "It's okay to take your time. Would you like me to explain this again?",
                "I'm here to help. What specific details would you like me to clarify?"
            ],
            'stressed': [
                "I notice you might be feeling stressed. Let's take this slowly and carefully.",
                "There's no rush. I'm here to make this easy for you.",
                "I understand this can be stressful. Let me help you through this.",
                "Take a deep breath. We'll handle this together, step by step."
            ],
            'confused': [
                "I sense some confusion. Let me explain this more clearly.",
                "No worries if this seems complicated. I'll break it down for you.",
                "I'm here to make this simple. Which part would you like me to clarify?",
                "Let me explain this in a different way that might be clearer."
            ],
            'worried': [
                "I understand your concern. Let me assure you that this is completely safe.",
                "Your security is my top priority. Would you like me to explain the security measures?",
                "I can see you're being cautious, which is good. Let me verify the details with you.",
                "It's natural to be careful with financial matters. Let's review everything together."
            ]
        }
        
        # Select appropriate response type
        if is_stressed:
            response_list = responses['stressed']
        elif is_uncertain:
            response_list = responses['uncertain']
        elif emotion == 'confused':
            response_list = responses['confused']
        elif emotion in ['worried', 'anxious', 'concerned']:
            response_list = responses['worried']
        else:
            response_list = responses['uncertain']
        
        # Context-specific additions
        if context == 'transfer':
            return response_list[0] + " I can show you the exact amount and recipient before confirming."
        elif context == 'loan':
            return response_list[0] + " I can explain the terms and conditions in detail if you'd like."
        else:
            return response_list[0]
    
    def generate_confirmation_prompt(self, action: str, details: Dict) -> str:
        """
        Generate clear confirmation prompt for user.
        
        Args:
            action: Action to confirm
            details: Action details
            
        Returns:
            Confirmation prompt
        """
        prompts = {
            'transfer': (
                f"Let me confirm: You want to transfer {details.get('formatted_amount', '')} "
                f"to {details.get('recipient', '')}. Is that correct?"
            ),
            'loan': (
                f"Just to confirm: You're interested in a {details.get('loan_type', '')} loan "
                f"of {details.get('formatted_amount', '')} at {details.get('interest_rate', '')}% interest. "
                f"Is this right?"
            ),
            'reminder': (
                f"To confirm: I'll remind you about {details.get('title', '')} "
                f"{'for ' + details.get('formatted_amount', '') if details.get('amount') else ''}. "
                f"Should I set this up?"
            )
        }
        
        return prompts.get(action, "Please confirm if you'd like me to proceed.")
    
    def provide_explanation(self, action: str, reason: str) -> str:
        """
        Provide explanation for why an action was taken or suggested.
        
        Args:
            action: Action taken
            reason: Reason for the action
            
        Returns:
            Explanation message
        """
        explanations = {
            'additional_auth': (
                f"I'm asking for additional verification because {reason}. "
                f"This is to ensure your account's security."
            ),
            'limit_exceeded': (
                f"The amount exceeds your set limit because {reason}. "
                f"I need to verify this transaction to protect your account."
            ),
            'suggestion': (
                f"I'm suggesting this because {reason}. "
                f"You're always in control and can decline if you prefer."
            ),
            'private_mode': (
                f"I'm switching to private mode because {reason}. "
                f"This protects your sensitive information."
            )
        }
        
        return explanations.get(action, f"I'm doing this because {reason}.")
    
    def handle_error_empathetically(self, error_type: str, context: Optional[str] = None) -> str:
        """
        Generate empathetic error message.
        
        Args:
            error_type: Type of error
            context: Error context
            
        Returns:
            User-friendly error message
        """
        messages = {
            'insufficient_balance': (
                "I'm sorry, but it looks like you don't have enough balance for this transaction. "
                "Would you like me to check your current balance?"
            ),
            'invalid_recipient': (
                "I couldn't find that beneficiary in your contacts. "
                "Could you spell the name again, or would you like to add them as a new beneficiary?"
            ),
            'authentication_failed': (
                "I'm having trouble verifying your identity. "
                "This could be due to background noise. Shall we try again or use a PIN instead?"
            ),
            'system_error': (
                "I apologize, but I'm experiencing a technical issue. "
                "Your account is safe. Would you like to try again in a moment?"
            ),
            'timeout': (
                "I didn't catch that. No worries - we can start over. "
                "What would you like to do?"
            )
        }
        
        return messages.get(error_type, "I encountered an issue, but don't worry. Let's try that again.")
    
    def celebrate_success(self, action: str, details: Dict) -> str:
        """
        Generate positive confirmation message.
        
        Args:
            action: Completed action
            details: Action details
            
        Returns:
            Success message
        """
        messages = {
            'transfer': (
                f"Great! I've successfully transferred {details.get('formatted_amount', '')} "
                f"to {details.get('recipient', '')}. "
                f"Your new balance is {details.get('formatted_balance', '')}."
            ),
            'balance_check': (
                f"Your current balance is {details.get('formatted_balance', '')}. "
                f"Is there anything else I can help you with?"
            ),
            'reminder_set': (
                f"Perfect! I've set a reminder for {details.get('title', '')}. "
                f"I'll notify you when it's time."
            )
        }
        
        return messages.get(action, "All done! How else can I assist you?")
