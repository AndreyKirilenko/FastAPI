import base64
import os
import secrets
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    # TELEGRAM_TOKEN: str = os.environ.get('TELEGRAM_TOKEN')
    TELEGRAM_TOKEN: str = '1618395277:AAFVBZ3P4QVozpBiwJyPZcyox2e_pPixxkA'
    TUNA_WEPHOOK_URL: str = os.environ.get('TUNA_WEPHOOK_URL')
    WEPHOOK_PATH: str = '/webhook'
    # REDIS_PORT: str = os.environ.get("REDIS_PORT")
    debug: bool = True

settings = Settings()