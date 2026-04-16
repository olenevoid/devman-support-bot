import logging
from logging.handlers import RotatingFileHandler

import requests

from config import (
    HTTP_PROXY,
    TELEGRAM_LOG_BOT_TOKEN,
    TELEGRAM_LOG_CHAT_ID,
    USE_PROXY,
)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
TG_LOG_FORMAT = "%(levelname)s: %(message)s"
LOG_FILE = "bot.log"
TG_MAX_MESSAGE_LENGTH = 4096


class TelegramHandler(logging.Handler):
    def __init__(self, bot_token: str, chat_id: str):
        super().__init__()
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def emit(self, record):
        log_entry = self.format(record)
        if len(log_entry) > TG_MAX_MESSAGE_LENGTH:
            log_entry = log_entry[:TG_MAX_MESSAGE_LENGTH]
        proxies = (
            {"https": HTTP_PROXY, "http": HTTP_PROXY} if USE_PROXY else None
        )
        try:
            requests.post(
                self.api_url,
                json={"chat_id": self.chat_id, "text": log_entry},
                proxies=proxies,
                timeout=10,
            )
        except Exception:
            pass


def setup_logging(level=logging.INFO) -> None:
    logging.basicConfig(format=LOG_FORMAT, level=level)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(file_handler)

    if TELEGRAM_LOG_BOT_TOKEN and TELEGRAM_LOG_CHAT_ID:
        tg_handler = TelegramHandler(
            TELEGRAM_LOG_BOT_TOKEN,
            TELEGRAM_LOG_CHAT_ID,
        )
        tg_handler.setLevel(logging.WARNING)
        tg_handler.setFormatter(logging.Formatter(TG_LOG_FORMAT))
        logging.getLogger().addHandler(tg_handler)
