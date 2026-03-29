"""Configuration management."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field, fields
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

_DEFAULT_PATH = Path.home() / ".config" / "live-tts" / "config.yaml"

VOICES = [
    "casual_female",
    "casual_male",
    "cheerful_female",
    "neutral_female",
    "neutral_male",
    "pt_male",
    "pt_female",
    "nl_male",
    "nl_female",
    "it_male",
    "it_female",
    "fr_male",
    "fr_female",
    "es_male",
    "es_female",
    "de_male",
    "de_female",
    "ar_male",
    "hi_male",
    "hi_female",
]


@dataclass
class Config:
    hotkey: str = "<ctrl>+<shift>+a"
    server_url: str = "http://localhost:8000"
    model_name: str = "mistralai/Voxtral-4B-TTS-2603"
    voice: str = "fr_male"
    response_format: str = "wav"

    @classmethod
    def load(cls, path: Path | None = None) -> Config:
        path = path or _DEFAULT_PATH
        if not path.exists():
            logger.info("No config at %s, using defaults", path)
            return cls()
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        known = {fld.name for fld in fields(cls)}
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)

    def save(self, path: Path | None = None) -> None:
        path = path or _DEFAULT_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {fld.name: getattr(self, fld.name) for fld in fields(self)}
        with open(path, "w") as f:
            yaml.safe_dump(data, f, default_flow_style=False)
