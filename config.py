import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    API_ID = os.getenv("API_ID")
    APP_API_HASH = os.getenv("APP_API_HASH")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CLIENT_PHONE_NUMBER = os.getenv("CLIENT_PHONE_NUMBER")
    # TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))
    USER_TO_LISTEN_TO = os.getenv("USER_TO_LISTEN_TO")
    USER_TO_FORWARD_TO = os.getenv("USER_TO_FORWARD_TO")
