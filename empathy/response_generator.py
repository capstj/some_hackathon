"""
Empathetic response generator for WhisPay.
Creates contextually appropriate and caring responses.
"""

from typing import Dict, Optional, List
from utils.helpers import create_greeting, get_time_of_day
from utils.logger import log


class ResponseGenerator:
    """Generates empathetic and contextual responses."""
    
    def __init__(self):
        """Initialize response generator."""
        log.info("Response generator initialized")
    
    def generate_greeting(self, user_name: Optional[str] = None, context: Optional[str] = None) -> str:
        """
        Generate personalized greeting.
        
        Args:
            user_name: User's name
            context: Greeting context
            
        Returns:
            Greeting message
        """
        base_greeting = create_greeting()
        
        if user_name:
            greeting = f"{base_greeting}, {user_name}"
        else:
            greeting = f"{base_greeting}"
        
        # Add context-specific message
        if context == 'first_time':
            greeting += ". I'm WhisPay, your voice banking assistant. I'm here to help you manage your finances easily and securely."
        elif context == 'returning':
            greeting += ". Welcome back! How can I assist you today?"
        else:
            greeting += ". How may I help you with your banking today?"
        
        return greeting
    
    def generate_help_message(self) -> str:
        """
        Generate help message explaining capabilities.
        
        Returns:
            Help message
        """
        return (
            "I can help you with many banking tasks. You can ask me to:\n"
            "• Check your account balance\n"
            "• Transfer money to your saved beneficiaries\n"
            "• View your transaction history\n"
            "• Get information about loans\n"
            "• Set payment reminders\n"
            "• Get spending summaries and insights\n\n"
            "Just speak naturally, and I'll understand what you need."
        )
    
    def generate_goodbye(self, user_name: Optional[str] = None) -> str:
        """
        Generate goodbye message.
        
        Args:
            user_name: User's name
            
        Returns:
            Goodbye message
        """
        time_of_day = get_time_of_day()
        
        if time_of_day == 'night':
            farewell = "Good night"
        else:
            farewell = "Have a great day"
        
        if user_name:
            return f"{farewell}, {user_name}! Feel free to reach out whenever you need banking assistance."
        else:
            return f"{farewell}! I'm always here when you need me."
    
    def generate_transaction_summary(self, transaction_data: Dict) -> str:
        """
        Generate clear transaction summary.
        
        Args:
            transaction_data: Transaction details
            
        Returns:
            Summary message
        """
        if transaction_data.get('success'):
            return (
                f"Transaction completed successfully. "
                f"{transaction_data.get('formatted_amount', '')} has been sent to "
                f"{transaction_data.get('recipient', '')}. "
                f"Your remaining balance is {transaction_data.get('formatted_balance', '')}. "
                f"Transaction ID: {transaction_data.get('transaction_id', '')}."
            )
        else:
            return f"I couldn't complete the transaction. {transaction_data.get('error', 'Please try again.')}"
    
    def generate_balance_response(self, balance_data: Dict, context: Optional[str] = None) -> str:
        """
        Generate balance information response.
        
        Args:
            balance_data: Balance details
            context: Response context
            
        Returns:
            Balance message
        """
        if not balance_data.get('success'):
            return f"I couldn't retrieve your balance. {balance_data.get('error', '')}"
        
        balance_msg = (
            f"Your {balance_data.get('account_type', '')} account balance is "
            f"{balance_data.get('formatted_balance', '')}."
        )
        
        if context == 'before_transfer':
            balance_msg += " Is there anything else you'd like to know before we proceed?"
        
        return balance_msg
    
    def generate_loan_info_response(self, loan_data: Dict) -> str:
        """
        Generate loan information response.
        
        Args:
            loan_data: Loan details
            
        Returns:
            Loan information message
        """
        if not loan_data.get('success'):
            return f"I couldn't get loan information. {loan_data.get('error', '')}"
        
        response = (
            f"For a {loan_data.get('loan_type', '')} loan, "
            f"the current interest rate is {loan_data.get('interest_rate', '')}% per annum. "
            f"You can borrow between {loan_data.get('min_amount', '')} and "
            f"{loan_data.get('max_amount', '')} rupees."
        )
        
        if loan_data.get('emi'):
            response += (
                f"\n\nFor a loan of {loan_data.get('formatted_amount', '')}, "
                f"your monthly EMI would be approximately {loan_data.get('formatted_emi', '')} "
                f"for {loan_data.get('tenure_months', '')} months. "
                f"The total amount payable would be {loan_data.get('formatted_total', '')}."
            )
        
        response += "\n\nWould you like to know more or proceed with an application?"
        
        return response
    
    def generate_history_summary(self, history_data: Dict) -> str:
        """
        Generate transaction history summary.
        
        Args:
            history_data: Transaction history
            
        Returns:
            History summary message
        """
        if not history_data.get('success'):
            return f"I couldn't retrieve your transaction history. {history_data.get('error', '')}"
        
        count = history_data.get('count', 0)
        if count == 0:
            return "You don't have any recent transactions."
        
        response = f"Here are your last {count} transactions:\n\n"
        
        for i, txn in enumerate(history_data.get('transactions', [])[:5], 1):
            date_str = txn.get('date').strftime('%B %d') if txn.get('date') else ''
            response += (
                f"{i}. {txn.get('formatted_amount', '')} to {txn.get('recipient', '')} "
                f"on {date_str}\n"
            )
        
        if count > 5:
            response += f"\n...and {count - 5} more transactions."
        
        return response
    
    def generate_proactive_suggestion_message(self, suggestions: List[Dict]) -> Optional[str]:
        """
        Generate message for proactive suggestions.
        
        Args:
            suggestions: List of suggestions
            
        Returns:
            Suggestion message or None
        """
        if not suggestions:
            return None
        
        # Get highest priority suggestion
        suggestion = suggestions[0]
        return suggestion.get('message', '')
    
    def generate_privacy_mode_message(self, info_type: str) -> str:
        """
        Generate message about privacy mode activation.
        
        Args:
            info_type: Type of information
            
        Returns:
            Privacy mode message
        """
        return (
            f"I've detected that you're in a public space. "
            f"For your privacy and security, I'll send your {info_type} "
            f"to your phone via SMS instead of speaking it aloud. "
            f"Please check your phone in a moment."
        )
    
    def generate_monthly_summary_response(self, summary_data: Dict) -> str:
        """
        Generate monthly spending summary response.
        
        Args:
            summary_data: Monthly summary data
            
        Returns:
            Summary message
        """
        if not summary_data.get('success'):
            return f"I couldn't generate the monthly summary. {summary_data.get('error', '')}"
        
        if summary_data.get('transaction_count', 0) == 0:
            return f"You didn't have any transactions in {summary_data.get('month_name', '')}."
        
        response = (
            f"Here's your spending summary for {summary_data.get('month_name', '')} {summary_data.get('year', '')}:\n\n"
            f"• Total spent: {summary_data.get('formatted_total', '')}\n"
            f"• Number of transactions: {summary_data.get('transaction_count', '')}\n\n"
        )
        
        if summary_data.get('top_recipients'):
            response += "Your top spending categories were:\n"
            for i, recipient in enumerate(summary_data.get('top_recipients', [])[:3], 1):
                response += (
                    f"{i}. {recipient.get('name', '')}: "
                    f"{recipient.get('formatted_amount', '')} "
                    f"({recipient.get('percentage', 0):.1f}%)\n"
                )
        
        return response
    
    def generate_error_recovery_message(self, error_context: str) -> str:
        """
        Generate message to recover from error gracefully.
        
        Args:
            error_context: Context where error occurred
            
        Returns:
            Recovery message
        """
        messages = {
            'speech_recognition': (
                "I'm sorry, I didn't quite catch that. Could you please repeat?"
            ),
            'voice_verification': (
                "I'm having trouble recognizing your voice. "
                "This might be due to background noise. "
                "Would you like to try again or use your PIN for verification?"
            ),
            'network': (
                "I'm experiencing connectivity issues. "
                "Please try again in a moment. Your data is safe."
            ),
            'unknown': (
                "I encountered an unexpected issue. "
                "Don't worry, your account is secure. "
                "Would you like to try again?"
            )
        }
        
        return messages.get(error_context, messages['unknown'])
    
    def add_empathy_layer(self, response: str, emotion: str) -> str:
        """
        Add empathetic touches to response based on detected emotion.
        
        Args:
            response: Base response
            emotion: Detected emotion
            
        Returns:
            Enhanced response
        """
        empathy_prefixes = {
            'stressed': "I understand this might be stressful. ",
            'uncertain': "I'm here to help make this clear. ",
            'confused': "Let me simplify this for you. ",
            'worried': "I assure you everything is secure. "
        }
        
        prefix = empathy_prefixes.get(emotion, "")
        return prefix + response if prefix else response
