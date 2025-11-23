"""
Configuration management for WhisPay application.
Loads settings from environment variables and provides centralized access.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="WhisPay", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Security
    secret_key: str = Field(default="change-me-in-production", env="SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_minutes: int = Field(default=30, env="JWT_EXPIRATION_MINUTES")
    
    # Voice Biometrics
    voice_biometric_threshold: float = Field(default=0.85, env="VOICE_BIOMETRIC_THRESHOLD")
    voice_sample_rate: int = Field(default=16000, env="VOICE_SAMPLE_RATE")
    voice_channels: int = Field(default=1, env="VOICE_CHANNELS")
    
    # Emotion Detection
    emotion_confidence_threshold: float = Field(default=0.7, env="EMOTION_CONFIDENCE_THRESHOLD")
    stress_detection_enabled: bool = Field(default=True, env="STRESS_DETECTION_ENABLED")
    
    # Trust Mode
    adaptive_trust_enabled: bool = Field(default=True, env="ADAPTIVE_TRUST_ENABLED")
    background_noise_threshold: float = Field(default=0.3, env="BACKGROUND_NOISE_THRESHOLD")
    high_risk_environment_detection: bool = Field(default=True, env="HIGH_RISK_ENVIRONMENT_DETECTION")
    
    # Transaction Limits
    default_transaction_limit: float = Field(default=10000.0, env="DEFAULT_TRANSACTION_LIMIT")
    high_value_threshold: float = Field(default=25000.0, env="HIGH_VALUE_THRESHOLD")
    require_reverification_above: float = Field(default=25000.0, env="REQUIRE_REVERIFICATION_ABOVE")
    
    # Private Mode
    private_mode_enabled: bool = Field(default=True, env="PRIVATE_MODE_ENABLED")
    sms_provider: str = Field(default="twilio", env="SMS_PROVIDER")
    twilio_account_sid: Optional[str] = Field(default=None, env="TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[str] = Field(default=None, env="TWILIO_AUTH_TOKEN")
    twilio_phone_number: Optional[str] = Field(default=None, env="TWILIO_PHONE_NUMBER")
    
    # WhatsApp
    whatsapp_enabled: bool = Field(default=False, env="WHATSAPP_ENABLED")
    whatsapp_api_key: Optional[str] = Field(default=None, env="WHATSAPP_API_KEY")
    
    # Database
    database_url: str = Field(default="sqlite:///./data/whispay.db", env="DATABASE_URL")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # NLP Models
    intent_model: str = Field(default="bert-base-uncased", env="INTENT_MODEL")
    emotion_model: str = Field(default="distilbert-base-uncased", env="EMOTION_MODEL")
    use_gpu: bool = Field(default=False, env="USE_GPU")
    
    # Speech Recognition
    speech_recognition_engine: str = Field(default="google", env="SPEECH_RECOGNITION_ENGINE")
    speech_language: str = Field(default="en-IN", env="SPEECH_LANGUAGE")
    speech_timeout: int = Field(default=5, env="SPEECH_TIMEOUT")
    speech_phrase_time_limit: int = Field(default=10, env="SPEECH_PHRASE_TIME_LIMIT")
    
    # Text-to-Speech
    tts_engine: str = Field(default="pyttsx3", env="TTS_ENGINE")
    tts_rate: int = Field(default=150, env="TTS_RATE")
    tts_volume: float = Field(default=0.9, env="TTS_VOLUME")
    tts_voice: str = Field(default="female", env="TTS_VOICE")
    
    # Predictive Features
    enable_predictions: bool = Field(default=True, env="ENABLE_PREDICTIONS")
    prediction_lookback_days: int = Field(default=90, env="PREDICTION_LOOKBACK_DAYS")
    monthly_summary_day: int = Field(default=1, env="MONTHLY_SUMMARY_DAY")
    recurring_transaction_threshold: int = Field(default=3, env="RECURRING_TRANSACTION_THRESHOLD")
    
    # Evaluation
    collect_metrics: bool = Field(default=True, env="COLLECT_METRICS")
    collect_feedback: bool = Field(default=True, env="COLLECT_FEEDBACK")
    metrics_export_path: str = Field(default="./data/metrics/", env="METRICS_EXPORT_PATH")
    
    # Cache
    cache_enabled: bool = Field(default=True, env="CACHE_ENABLED")
    cache_ttl_seconds: int = Field(default=300, env="CACHE_TTL_SECONDS")
    
    # Logging
    log_file: str = Field(default="./logs/whispay.log", env="LOG_FILE")
    log_rotation: str = Field(default="10 MB", env="LOG_ROTATION")
    log_retention: str = Field(default="30 days", env="LOG_RETENTION")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance."""
    return settings
