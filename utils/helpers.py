"""
Helper utility functions for WhisPay.
"""

import re
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import hashlib
import json


def extract_amount(text: str) -> Optional[float]:
    """
    Extract monetary amount from text.
    
    Args:
        text: Input text containing amount
        
    Returns:
        Extracted amount as float or None
    """
    # Match patterns like "5000", "5,000", "5000 rupees", "₹5000"
    patterns = [
        r'₹?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
        r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:rupees?|rs\.?|inr)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(',', '')
            try:
                return float(amount_str)
            except ValueError:
                continue
    
    return None


def extract_recipient(text: str) -> Optional[str]:
    """
    Extract recipient name from text.
    
    Args:
        text: Input text containing recipient
        
    Returns:
        Recipient name or None
    """
    # Match patterns like "to Mom", "to John", "transfer to Alice"
    patterns = [
        r'to\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)',
        r'for\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None


def format_currency(amount: float, currency: str = "₹") -> str:
    """
    Format amount as currency string.
    
    Args:
        amount: Amount to format
        currency: Currency symbol
        
    Returns:
        Formatted currency string
    """
    return f"{currency}{amount:,.2f}"


def hash_voice_print(voice_data: bytes) -> str:
    """
    Create a hash of voice biometric data.
    
    Args:
        voice_data: Raw voice biometric data
        
    Returns:
        SHA-256 hash of voice data
    """
    return hashlib.sha256(voice_data).hexdigest()


def calculate_similarity(vec1: list, vec2: list) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Similarity score between 0 and 1
    """
    import numpy as np
    
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


def is_within_date_range(
    date: datetime,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> bool:
    """
    Check if date is within specified range.
    
    Args:
        date: Date to check
        start_date: Start of range (inclusive)
        end_date: End of range (inclusive)
        
    Returns:
        True if date is within range
    """
    if start_date and date < start_date:
        return False
    if end_date and date > end_date:
        return False
    return True


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing potentially harmful characters.
    
    Args:
        text: Raw input text
        
    Returns:
        Sanitized text
    """
    # Remove control characters and excessive whitespace
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number string
        
    Returns:
        True if valid phone number
    """
    # Basic validation for Indian phone numbers
    pattern = r'^(\+91)?[6-9]\d{9}$'
    return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))


def get_time_of_day() -> str:
    """
    Get current time of day category.
    
    Returns:
        'morning', 'afternoon', 'evening', or 'night'
    """
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'night'


def create_greeting() -> str:
    """
    Create time-appropriate greeting.
    
    Returns:
        Greeting message
    """
    time_of_day = get_time_of_day()
    greetings = {
        'morning': 'Good morning',
        'afternoon': 'Good afternoon',
        'evening': 'Good evening',
        'night': 'Good evening'
    }
    return greetings.get(time_of_day, 'Hello')


def serialize_json(obj: Any) -> str:
    """
    Serialize object to JSON with datetime handling.
    
    Args:
        obj: Object to serialize
        
    Returns:
        JSON string
    """
    def default(o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")
    
    return json.dumps(obj, default=default)


def mask_sensitive_data(text: str, mask_char: str = "*") -> str:
    """
    Mask sensitive information in text.
    
    Args:
        text: Text containing sensitive data
        mask_char: Character to use for masking
        
    Returns:
        Masked text
    """
    # Mask account numbers (keep last 4 digits)
    text = re.sub(r'\b\d{8,16}\b', lambda m: mask_char * (len(m.group()) - 4) + m.group()[-4:], text)
    
    # Mask OTPs
    text = re.sub(r'\b\d{4,6}\b(?=.*otp|password|pin)', mask_char * 4, text, flags=re.IGNORECASE)
    
    return text
