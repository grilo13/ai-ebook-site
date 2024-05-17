import os
import secrets

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'AI Ebook Generator'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    LOG_LEVEL: str = os.getenv('LOG_LEVEL')


settings = Settings()
