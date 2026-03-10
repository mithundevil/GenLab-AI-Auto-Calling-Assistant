import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "GenLab AI Calling Assistant"
    DEBUG: bool = True
    PORT: int = 8000
    
    # Twilio Settings
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    # AI Settings (Groq - Using Llama for high speed)
    GROK_API_KEY: str = os.getenv("GROK_API_KEY", "")
    GROK_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    GROK_MODEL: str = "llama-3.3-70b-versatile"
    
    # Database Settings
    DB_PATH: str = "database/leads.db"
    
    # Base URL for Webhooks (Update after deployment)
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

settings = Settings()
