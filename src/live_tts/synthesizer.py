"""TTS synthesis via Voxtral vLLM server."""

from __future__ import annotations

import io
import logging

import httpx
import numpy as np
import soundfile as sf

from .config import Config

logger = logging.getLogger(__name__)


class Synthesizer:
    """Sends text to a vLLM server running Voxtral and returns audio."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._client = httpx.Client(timeout=120.0)

    def synthesize(self, text: str) -> tuple[np.ndarray, int]:
        """
        Synthesize text to audio.

        Returns a tuple of (audio_array, sample_rate).
        """
        url = f"{self._config.server_url}/v1/audio/speech"
        payload = {
            "input": text,
            "model": self._config.model_name,
            "response_format": self._config.response_format,
            "voice": self._config.voice,
        }

        logger.info("Sending TTS request (%d chars, voice=%s)", len(text), self._config.voice)
        response = self._client.post(url, json=payload)
        response.raise_for_status()

        audio_array, sample_rate = sf.read(
            io.BytesIO(response.content), dtype="float32"
        )
        logger.info(
            "Received audio: %d samples at %d Hz (%.1fs)",
            len(audio_array),
            sample_rate,
            len(audio_array) / sample_rate,
        )
        return audio_array, sample_rate

    def close(self) -> None:
        self._client.close()
