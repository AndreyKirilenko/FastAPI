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
    TUNA_WEBHOOK_URL: str = os.environ.get('TUNA_WEBHOOK_URL')
    # TUNA_WEBHOOK_URL: str = 'https://n35ebp-83-220-90-104.ru.tuna.am'
    WEBHOOK_PATH: str = '/webhook'
    WB_TOKEN: str = os.environ.get('WB_TOKEN')
    # REDIS_PORT: str = os.environ.get("REDIS_PORT")
    debug: bool = True

    # POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    # POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    # POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
    # POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5432) # default postgres port is 5432
    # POSTGRES_DB : str = os.getenv("POSTGRES_DB","tdd")
    # DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Settings()