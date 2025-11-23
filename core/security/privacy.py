"""
Privacy mode for WhisPay.
Handles secure transmission of sensitive information via SMS/WhatsApp.
"""

from typing import Optional, Dict
from utils.logger import log
from app.config import settings
import requests


class PrivacyMode:
    """Manages private mode for secure information delivery."""
    
    def __init__(self):
        """Initialize privacy mode."""
        self.enabled = settings.private_mode_enabled
        log.info(f"Privacy mode initialized (enabled: {self.enabled})")
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        """
        Send SMS message using configured provider.
        
        Args:
            phone_number: Recipient phone number
            message: Message to send
            
        Returns:
            True if sent successfully
        """
        if not self.enabled:
            log.warning("Privacy mode not enabled")
            return False
        
        provider = settings.sms_provider.lower()
        
        if provider == "twilio":
            return self._send_via_twilio(phone_number, message)
        else:
            log.error(f"Unsupported SMS provider: {provider}")
            return False
    
    def _send_via_twilio(self, phone_number: str, message: str) -> bool:
        """
        Send SMS via Twilio.
        
        Args:
            phone_number: Recipient phone number
            message: Message content
            
        Returns:
            True if sent successfully
        """
        try:
            from twilio.rest import Client
            
            if not settings.twilio_account_sid or not settings.twilio_auth_token:
                log.error("Twilio credentials not configured")
                return False
            
            client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            
            message_obj = client.messages.create(
                body=message,
                from_=settings.twilio_phone_number,
                to=phone_number
            )
            
            log.info(f"SMS sent successfully (SID: {message_obj.sid})")
            return True
            
        except Exception as e:
            log.error(f"Error sending SMS via Twilio: {e}")
            return False
    
    def send_whatsapp(self, phone_number: str, message: str) -> bool:
        """
        Send WhatsApp message.
        
        Args:
            phone_number: Recipient phone number
            message: Message to send
            
        Returns:
            True if sent successfully
        """
        if not self.enabled or not settings.whatsapp_enabled:
            log.warning("WhatsApp not enabled")
            return False
        
        try:
            # Using Twilio WhatsApp API
            from twilio.rest import Client
            
            if not settings.twilio_account_sid or not settings.twilio_auth_token:
                log.error("Twilio credentials not configured")
                return False
            
            client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            
            message_obj = client.messages.create(
                body=message,
                from_=f'whatsapp:{settings.twilio_phone_number}',
                to=f'whatsapp:{phone_number}'
            )
            
            log.info(f"WhatsApp message sent successfully (SID: {message_obj.sid})")
            return True
            
        except Exception as e:
            log.error(f"Error sending WhatsApp message: {e}")
            return False
    
    def send_secure_info(
        self,
        user_phone: str,
        info_type: str,
        info_value: str,
        preferred_channel: str = "sms"
    ) -> bool:
        """
        Send sensitive information securely.
        
        Args:
            user_phone: User's phone number
            info_type: Type of information (balance, otp, etc.)
            info_value: The actual information
            preferred_channel: 'sms' or 'whatsapp'
            
        Returns:
            True if sent successfully
        """
        # Format message based on info type
        message = self._format_secure_message(info_type, info_value)
        
        # Send via preferred channel
        if preferred_channel == "whatsapp" and settings.whatsapp_enabled:
            success = self.send_whatsapp(user_phone, message)
        else:
            success = self.send_sms(user_phone, message)
        
        if success:
            log.info(f"Secure info ({info_type}) sent to user via {preferred_channel}")
        else:
            log.error(f"Failed to send secure info ({info_type}) to user")
        
        return success
    
    def _format_secure_message(self, info_type: str, info_value: str) -> str:
        """
        Format message for secure transmission.
        
        Args:
            info_type: Type of information
            info_value: The value
            
        Returns:
            Formatted message
        """
        templates = {
            'balance': f'WhisPay: Your account balance is {info_value}. This message will not be spoken aloud for your privacy.',
            'otp': f'WhisPay: Your verification code is {info_value}. Valid for 5 minutes. Do not share this code.',
            'transaction_confirm': f'WhisPay: {info_value}',
            'account_details': f'WhisPay: {info_value}. This information has been sent privately for your security.',
        }
        
        return templates.get(info_type, f'WhisPay: {info_value}')
    
    def should_use_private_mode(
        self,
        info_type: str,
        environmental_noise: float,
        nearby_people: bool = False
    ) -> bool:
        """
        Determine if private mode should be used.
        
        Args:
            info_type: Type of information to share
            environmental_noise: Noise level (0-1)
            nearby_people: Whether people are nearby
            
        Returns:
            True if private mode recommended
        """
        # Always use private mode for sensitive info
        sensitive_info = ['balance', 'otp', 'account_number', 'transaction_details']
        if info_type in sensitive_info:
            return True
        
        # Use private mode in noisy environments
        if environmental_noise > settings.background_noise_threshold:
            return True
        
        # Use private mode if people are nearby
        if nearby_people:
            return True
        
        return False
    
    def generate_privacy_prompt(self) -> str:
        """
        Generate prompt asking user about privacy preference.
        
        Returns:
            Privacy preference question
        """
        return (
            "I can share this information in two ways: "
            "I can speak it aloud, or send it privately to your phone via SMS. "
            "Which would you prefer?"
        )
