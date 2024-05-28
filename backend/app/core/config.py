import os
import secrets

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'AI Ebook Generator'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    LOG_LEVEL: str = os.getenv('LOG_LEVEL')
    RESEND_API_KEY: str = os.getenv('RESEND_API_KEY')
    EMAIL_SENDER: str = os.getenv('EMAIL_SENDER')

    # stripe variables
    STRIPE_API_SECRET: str = os.getenv('STRIPE_API_SECRET')
    STRIPE_ENDPOINT_SECRET: str = os.getenv('STRIPE_ENDPOINT_SECRET')
    FRONTEND_URL: str = os.getenv('FRONTEND_URL')


settings = Settings()
