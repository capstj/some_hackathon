"""
Entity extraction module for WhisPay.
Extracts structured information from user input.
"""

import re
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
from utils.logger import log
from utils.helpers import extract_amount, extract_recipient, sanitize_input


class EntityExtractor:
    """Extracts entities like amounts, recipients, dates from text."""
    
    def __init__(self):
        """Initialize the entity extractor."""
        log.info("Entity extractor initialized")
    
    def extract(self, text: str) -> Dict[str, Any]:
        """
        Extract all entities from text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of extracted entities
        """
        text = sanitize_input(text)
        
        entities = {
            'amount': self.extract_amount(text),
            'recipient': self.extract_recipient(text),
            'date': self.extract_date(text),
            'account_type': self.extract_account_type(text),
            'loan_type': self.extract_loan_type(text),
            'time_period': self.extract_time_period(text),
            'frequency': self.extract_frequency(text)
        }
        
        # Remove None values
        entities = {k: v for k, v in entities.items() if v is not None}
        
        if entities:
            log.info(f"Extracted entities: {entities}")
        
        return entities
    
    def extract_amount(self, text: str) -> Optional[float]:
        """Extract monetary amount from text."""
        return extract_amount(text)
    
    def extract_recipient(self, text: str) -> Optional[str]:
        """Extract recipient name from text."""
        return extract_recipient(text)
    
    def extract_date(self, text: str) -> Optional[datetime]:
        """
        Extract date/time from text.
        
        Args:
            text: Input text
            
        Returns:
            datetime object or None
        """
        text_lower = text.lower()
        
        # Relative dates
        if 'today' in text_lower:
            return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        elif 'tomorrow' in text_lower:
            return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        elif 'yesterday' in text_lower:
            return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        
        # Specific dates (DD/MM/YYYY or DD-MM-YYYY)
        date_pattern = r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b'
        match = re.search(date_pattern, text)
        if match:
            try:
                day, month, year = match.groups()
                year = int(year)
                if year < 100:
                    year += 2000
                return datetime(year, int(month), int(day))
            except ValueError:
                pass
        
        return None
    
    def extract_account_type(self, text: str) -> Optional[str]:
        """
        Extract account type from text.
        
        Args:
            text: Input text
            
        Returns:
            Account type or None
        """
        text_lower = text.lower()
        
        if 'saving' in text_lower:
            return 'savings'
        elif 'current' in text_lower:
            return 'current'
        elif 'salary' in text_lower:
            return 'salary'
        
        return None
    
    def extract_loan_type(self, text: str) -> Optional[str]:
        """
        Extract loan type from text.
        
        Args:
            text: Input text
            
        Returns:
            Loan type or None
        """
        text_lower = text.lower()
        
        loan_types = {
            'personal': ['personal', 'individual'],
            'home': ['home', 'housing', 'house', 'property'],
            'car': ['car', 'auto', 'vehicle'],
            'education': ['education', 'student', 'study'],
            'business': ['business', 'commercial', 'enterprise']
        }
        
        for loan_type, keywords in loan_types.items():
            if any(keyword in text_lower for keyword in keywords):
                return loan_type
        
        return None
    
    def extract_time_period(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract time period (last week, this month, etc.).
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with start and end dates
        """
        text_lower = text.lower()
        now = datetime.now()
        
        # This week
        if 'this week' in text_lower:
            start = now - timedelta(days=now.weekday())
            return {
                'start': start.replace(hour=0, minute=0, second=0, microsecond=0),
                'end': now,
                'label': 'this week'
            }
        
        # Last week
        if 'last week' in text_lower:
            start = now - timedelta(days=now.weekday() + 7)
            end = start + timedelta(days=6)
            return {
                'start': start.replace(hour=0, minute=0, second=0, microsecond=0),
                'end': end.replace(hour=23, minute=59, second=59),
                'label': 'last week'
            }
        
        # This month
        if 'this month' in text_lower:
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return {
                'start': start,
                'end': now,
                'label': 'this month'
            }
        
        # Last month
        if 'last month' in text_lower:
            first_this_month = now.replace(day=1)
            last_day_prev_month = first_this_month - timedelta(days=1)
            first_prev_month = last_day_prev_month.replace(day=1)
            return {
                'start': first_prev_month.replace(hour=0, minute=0, second=0, microsecond=0),
                'end': last_day_prev_month.replace(hour=23, minute=59, second=59),
                'label': 'last month'
            }
        
        # Last N days
        days_pattern = r'last\s+(\d+)\s+days?'
        match = re.search(days_pattern, text_lower)
        if match:
            days = int(match.group(1))
            start = now - timedelta(days=days)
            return {
                'start': start.replace(hour=0, minute=0, second=0, microsecond=0),
                'end': now,
                'label': f'last {days} days'
            }
        
        return None
    
    def extract_frequency(self, text: str) -> Optional[str]:
        """
        Extract payment frequency (daily, weekly, monthly).
        
        Args:
            text: Input text
            
        Returns:
            Frequency string or None
        """
        text_lower = text.lower()
        
        frequencies = {
            'daily': ['daily', 'every day', 'each day'],
            'weekly': ['weekly', 'every week', 'each week'],
            'monthly': ['monthly', 'every month', 'each month'],
            'yearly': ['yearly', 'annually', 'every year']
        }
        
        for frequency, keywords in frequencies.items():
            if any(keyword in text_lower for keyword in keywords):
                return frequency
        
        return None
    
    def extract_contact_info(self, text: str) -> Optional[Dict[str, str]]:
        """
        Extract phone number or email from text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with contact info or None
        """
        # Phone number (Indian format)
        phone_pattern = r'(\+91|0)?[6-9]\d{9}'
        phone_match = re.search(phone_pattern, text)
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        
        contact = {}
        if phone_match:
            contact['phone'] = phone_match.group()
        if email_match:
            contact['email'] = email_match.group()
        
        return contact if contact else None
