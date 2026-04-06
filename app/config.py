from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:  # noqa: BLE001
    def load_dotenv() -> None:
        return None


load_dotenv()


@dataclass(slots=True)
class AppConfig:
    openai_api_key: str | None
    openai_model: str
    log_level: str
    data_dir: Path
    default_output_dir: Path



def get_config() -> AppConfig:
    return AppConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        log_level=os.getenv("APP_LOG_LEVEL", "INFO"),
        data_dir=Path("data"),
        default_output_dir=Path("outputs"),
    )
