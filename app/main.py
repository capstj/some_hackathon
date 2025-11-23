"""
Main WhisPay application.
Orchestrates all components for voice banking interactions.
"""

from typing import Optional, Dict, Any
from datetime import datetime
import numpy as np

from utils.logger import log
from app.config import settings

# Core components
from core.speech.recognizer import SpeechRecognizer
from core.speech.synthesizer import SpeechSynthesizer
from core.speech.voice_biometrics import VoiceBiometrics
from core.nlp.intent_detector import IntentDetector
from core.nlp.entity_extractor import EntityExtractor
from core.nlp.emotion_analyzer import EmotionAnalyzer

# Security
from core.security.authentication import AuthenticationManager
from core.security.trust_mode import AdaptiveTrustMode, TrustLevel
from core.security.privacy import PrivacyMode

# Banking
from banking.operations import BankingOperations
from banking.predictor import BankingPredictor
from banking.database import db

# Empathy
from empathy.ecc import EmotionalConfidenceCheck
from empathy.response_generator import ResponseGenerator


class WhisPayAssistant:
    """Main WhisPay voice banking assistant."""
    
    def __init__(self):
        """Initialize WhisPay assistant."""
        log.info("Initializing WhisPay assistant...")
        
        # Core components
        self.recognizer = SpeechRecognizer()
        self.synthesizer = SpeechSynthesizer()
        self.voice_biometrics = VoiceBiometrics()
        self.intent_detector = IntentDetector()
        self.entity_extractor = EntityExtractor()
        self.emotion_analyzer = EmotionAnalyzer()
        
        # Security
        self.auth_manager = AuthenticationManager()
        self.trust_mode = AdaptiveTrustMode()
        self.privacy_mode = PrivacyMode()
        
        # Banking
        self.banking_ops = BankingOperations()
        self.predictor = BankingPredictor()
        
        # Empathy
        self.ecc = EmotionalConfidenceCheck()
        self.response_gen = ResponseGenerator()
        
        # Session state
        self.current_user_id: Optional[str] = None
        self.session_token: Optional[str] = None
        self.conversation_context: Dict[str, Any] = {}
        self.awaiting_confirmation: bool = False
        self.pending_action: Optional[Dict] = None
        
        log.info("WhisPay assistant initialized successfully")
    
    def start(self):
        """Start the WhisPay assistant."""
        log.info("WhisPay assistant starting...")
        
        # Greet user
        greeting = self.response_gen.generate_greeting(context='first_time')
        self.speak(greeting)
        
        # Authenticate user
        if not self.authenticate_user():
            self.speak("I couldn't verify your identity. For security, I'll need to end this session.")
            return
        
        # Main conversation loop
        self.conversation_loop()
    
    def authenticate_user(self) -> bool:
        """
        Authenticate user using voice biometrics or PIN.
        
        Returns:
            True if authentication successful
        """
        # Check if this is first time user (no voice prints enrolled)
        import os
        voice_prints_dir = os.path.join(self.voice_biometrics.voice_prints_dir)
        has_enrolled_users = os.path.exists(voice_prints_dir) and len(os.listdir(voice_prints_dir)) > 0
        
        if not has_enrolled_users:
            self.speak(
                "I notice this is your first time using WhisPay. "
                "For security, I'll verify your identity with your PIN first, "
                "then we can enroll your voice for future logins. "
                "Please speak your 4-digit PIN."
            )
            if self.authenticate_with_pin():
                # Offer to enroll voice
                self.speak(
                    "Great! Now, would you like to enroll your voice for faster authentication next time? "
                    "Say 'yes' to enroll, or 'no' to skip."
                )
                response = self.listen()
                if response and 'yes' in response.lower():
                    self.enroll_voice_print()
                return True
            return False
        
        # Try voice authentication for returning users
        self.speak("Please say a few words so I can verify your identity.")
        
        # Record voice sample
        audio_data = self.recognizer.get_audio_data(duration=3)
        if audio_data is None:
            return False
        
        # Try to identify user
        result = self.voice_biometrics.identify_user(audio_data)
        
        if result:
            user_id, confidence = result
            self.current_user_id = user_id
            
            # Assess trust level
            noise_level = self.recognizer.measure_background_noise()
            trust_level = self.trust_mode.assess_trust_level(
                noise_level=noise_level,
                voice_confidence=confidence
            )
            
            # Create session
            self.session_token = self.auth_manager.create_session(
                user_id, 'voice_biometric'
            )
            
            # Get user info
            user = self.banking_ops.get_user(user_id)
            user_name = user.name if user else None
            
            # Welcome message
            message = self.trust_mode.generate_trust_message(trust_level)
            greeting = self.response_gen.generate_greeting(user_name, 'returning')
            self.speak(f"{greeting} {message}")
            
            # Check for proactive suggestions
            self.check_proactive_suggestions()
            
            return True
        else:
            self.speak(
                "I'm having trouble recognizing your voice. "
                "Let's try using your PIN for verification. "
                "Please speak your 4-digit PIN."
            )
            return self.authenticate_with_pin()
    
    def authenticate_with_pin(self) -> bool:
        """
        Authenticate user with PIN.
        
        Returns:
            True if authentication successful
        """
        pin_text = self.listen()
        if not pin_text:
            return False
        
        # Extract PIN from text
        import re
        # Handle both spoken "1 2 3 4" and "1234"
        digits = ''.join(re.findall(r'\d', pin_text))
        
        if len(digits) < 4:
            self.speak("I didn't catch a valid 4-digit PIN. Please try again.")
            return False
        
        pin = digits[:4]  # Take first 4 digits
        
        # For demo, use default user
        user_id = "user001"
        user = self.banking_ops.get_user(user_id)
        
        if user and self.auth_manager.verify_pin(pin, user.pin_hash):
            self.current_user_id = user_id
            self.session_token = self.auth_manager.create_session(user_id, 'pin')
            
            greeting = self.response_gen.generate_greeting(user.name, 'returning')
            self.speak(greeting)
            
            self.check_proactive_suggestions()
            return True
        else:
            self.speak("The PIN you entered is incorrect. Please try again.")
            return False
    
    def enroll_voice_print(self):
        """Enroll user's voice for biometric authentication."""
        try:
            self.speak(
                "Great! I'll record your voice now. "
                "Please say a few sentences so I can learn your voice. "
                "For example, you could say: 'I want to check my account balance and transfer money.'"
            )
            
            # Record voice sample
            audio_data = self.recognizer.get_audio_data(duration=5)
            if audio_data is None:
                self.speak("I couldn't record your voice. Let's try this again later.")
                return
            
            # Enroll the voice
            success = self.voice_biometrics.enroll_user(self.current_user_id, audio_data)
            
            if success:
                self.speak(
                    "Perfect! Your voice has been enrolled successfully. "
                    "Next time, you can just say a few words and I'll recognize you automatically."
                )
            else:
                self.speak(
                    "I had trouble enrolling your voice. You can try again later "
                    "or continue using your PIN for authentication."
                )
        except Exception as e:
            log.error(f"Error enrolling voice: {e}")
            self.speak("There was an issue enrolling your voice. Let's continue for now.")
    
    def conversation_loop(self):
        """Main conversation loop."""
        while True:
            try:
                # Listen for user input
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if self.is_exit_command(user_input):
                    self.handle_goodbye()
                    break
                
                # Process the input
                self.process_user_input(user_input)
                
            except KeyboardInterrupt:
                log.info("Interrupted by user")
                self.handle_goodbye()
                break
            except Exception as e:
                log.error(f"Error in conversation loop: {e}")
                self.speak(self.response_gen.generate_error_recovery_message('unknown'))
    
    def listen(self) -> Optional[str]:
        """
        Listen for user speech input.
        
        Returns:
            Recognized text or None
        """
        return self.recognizer.listen()
    
    def speak(self, text: str):
        """
        Speak text to user.
        
        Args:
            text: Text to speak
        """
        self.synthesizer.speak(text)
    
    def process_user_input(self, user_input: str):
        """
        Process user input and generate response.
        
        Args:
            user_input: User's spoken input
        """
        start_time = datetime.now()
        
        # Perform emotional confidence check
        ecc_result = self.ecc.check_confidence(user_input, context=self.conversation_context.get('action'))
        
        if ecc_result.get('should_intervene'):
            self.speak(ecc_result.get('response'))
            # Wait for user response before proceeding
            return
        
        # Handle confirmation if awaiting
        if self.awaiting_confirmation:
            self.handle_confirmation(user_input)
            return
        
        # Detect intent
        intent_result = self.intent_detector.detect(user_input)
        intent = intent_result.get('intent')
        confidence = intent_result.get('confidence', 0)
        
        log.info(f"Intent: {intent} (confidence: {confidence:.2f})")
        
        # Extract entities
        entities = self.entity_extractor.extract(user_input)
        
        # Route to appropriate handler
        response = self.route_intent(intent, entities, user_input)
        
        # Calculate response time
        response_time = (datetime.now() - start_time).total_seconds()
        log.info(f"Response time: {response_time:.2f}s")
        
        # Speak response
        if response:
            self.speak(response)
    
    def route_intent(self, intent: str, entities: Dict, user_input: str) -> Optional[str]:
        """
        Route intent to appropriate handler.
        
        Args:
            intent: Detected intent
            entities: Extracted entities
            user_input: Original user input
            
        Returns:
            Response text
        """
        handlers = {
            'check_balance': self.handle_check_balance,
            'transfer_money': self.handle_transfer,
            'transaction_history': self.handle_history,
            'loan_inquiry': self.handle_loan,
            'set_reminder': self.handle_reminder,
            'monthly_summary': self.handle_monthly_summary,
            'help': self.handle_help,
            'greeting': self.handle_greeting,
            'thank_you': self.handle_thank_you,
            'goodbye': self.handle_goodbye
        }
        
        handler = handlers.get(intent)
        if handler:
            return handler(entities)
        else:
            return "I'm not sure I understand. Could you rephrase that?"
    
    def handle_check_balance(self, entities: Dict) -> str:
        """Handle balance check request."""
        account_type = entities.get('account_type')
        result = self.banking_ops.check_balance(self.current_user_id, account_type)
        return self.response_gen.generate_balance_response(result)
    
    def handle_transfer(self, entities: Dict) -> str:
        """Handle money transfer request."""
        amount = entities.get('amount')
        recipient = entities.get('recipient')
        
        if not amount or not recipient:
            return "To transfer money, I need to know the amount and the recipient. Could you provide both?"
        
        # Store pending action and request confirmation
        self.pending_action = {
            'type': 'transfer',
            'amount': amount,
            'recipient': recipient
        }
        
        self.awaiting_confirmation = True
        self.conversation_context['action'] = 'transfer'
        
        from utils.helpers import format_currency
        details = {
            'formatted_amount': format_currency(amount, '₹'),
            'recipient': recipient
        }
        
        return self.ecc.generate_confirmation_prompt('transfer', details)
    
    def handle_confirmation(self, user_input: str):
        """Handle user confirmation response."""
        intent_result = self.intent_detector.detect(user_input)
        intent = intent_result.get('intent')
        
        if intent == 'confirm_action':
            # Execute pending action
            if self.pending_action:
                response = self.execute_pending_action()
                self.speak(response)
        elif intent == 'deny_action':
            self.speak("No problem. The action has been cancelled. What else can I help you with?")
        else:
            self.speak("I didn't catch that. Please say 'yes' to confirm or 'no' to cancel.")
            return
        
        # Reset confirmation state
        self.awaiting_confirmation = False
        self.pending_action = None
        self.conversation_context.clear()
    
    def execute_pending_action(self) -> str:
        """Execute the pending action."""
        if not self.pending_action:
            return "There's no pending action to execute."
        
        action_type = self.pending_action.get('type')
        
        if action_type == 'transfer':
            result = self.banking_ops.transfer_money(
                self.current_user_id,
                self.pending_action['recipient'],
                self.pending_action['amount']
            )
            return self.response_gen.generate_transaction_summary(result)
        
        return "I couldn't execute that action."
    
    def handle_history(self, entities: Dict) -> str:
        """Handle transaction history request."""
        time_period = entities.get('time_period')
        
        start_date = time_period.get('start') if time_period else None
        end_date = time_period.get('end') if time_period else None
        
        result = self.banking_ops.get_transaction_history(
            self.current_user_id,
            limit=10,
            start_date=start_date,
            end_date=end_date
        )
        
        return self.response_gen.generate_history_summary(result)
    
    def handle_loan(self, entities: Dict) -> str:
        """Handle loan inquiry."""
        loan_type = entities.get('loan_type', 'personal')
        amount = entities.get('amount')
        
        result = self.banking_ops.inquire_loan(self.current_user_id, loan_type, amount)
        return self.response_gen.generate_loan_info_response(result)
    
    def handle_reminder(self, entities: Dict) -> str:
        """Handle set reminder request."""
        # For simplicity, create a basic reminder
        return "I can set payment reminders for you. What should I remind you about?"
    
    def handle_monthly_summary(self, entities: Dict) -> str:
        """Handle monthly summary request."""
        result = self.predictor.get_monthly_summary(self.current_user_id)
        return self.response_gen.generate_monthly_summary_response(result)
    
    def handle_help(self, entities: Dict) -> str:
        """Handle help request."""
        return self.response_gen.generate_help_message()
    
    def handle_greeting(self, entities: Dict) -> str:
        """Handle greeting."""
        user = self.banking_ops.get_user(self.current_user_id)
        return self.response_gen.generate_greeting(user.name if user else None)
    
    def handle_thank_you(self, entities: Dict) -> str:
        """Handle thank you."""
        return "You're welcome! Happy to help. Is there anything else you need?"
    
    def handle_goodbye(self) -> str:
        """Handle goodbye."""
        user = self.banking_ops.get_user(self.current_user_id)
        farewell = self.response_gen.generate_goodbye(user.name if user else None)
        self.speak(farewell)
        
        # End session
        if self.session_token:
            self.auth_manager.end_session(self.session_token)
        
        return farewell
    
    def is_exit_command(self, text: str) -> bool:
        """Check if input is an exit command."""
        exit_patterns = ['bye', 'goodbye', 'exit', 'quit', 'stop', 'end']
        return any(pattern in text.lower() for pattern in exit_patterns)
    
    def check_proactive_suggestions(self):
        """Check and present proactive suggestions."""
        if not settings.enable_predictions:
            return
        
        suggestions = self.predictor.get_proactive_suggestions(self.current_user_id)
        
        if suggestions:
            message = self.response_gen.generate_proactive_suggestion_message(suggestions)
            if message:
                self.speak(message)


def main():
    """Main entry point."""
    log.info("=" * 50)
    log.info("Starting WhisPay - Voice Banking Assistant")
    log.info("=" * 50)
    
    # Initialize database with sample data (for demo)
    db.create_sample_data()
    
    # Create and start assistant
    assistant = WhisPayAssistant()
    assistant.start()
    
    log.info("WhisPay session ended")


if __name__ == "__main__":
    main()
