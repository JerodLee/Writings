"""Telegram alert sender."""

from __future__ import annotations

import logging
import requests

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    @property
    def enabled(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    def send_message(self, text: str) -> bool:
        """Send message to Telegram. Returns True on success."""
        if not self.enabled:
            logger.warning("Telegram credentials missing. Skipping message.")
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"}

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except Exception as exc:
            logger.error("Failed to send Telegram message: %s", exc)
            return False
