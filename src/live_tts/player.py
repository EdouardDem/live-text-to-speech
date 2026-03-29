"""Audio playback."""

from __future__ import annotations

import logging
import threading

import numpy as np
import sounddevice as sd

logger = logging.getLogger(__name__)


class Player:
    """Plays audio through the default output device."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._playing = False

    @property
    def playing(self) -> bool:
        return self._playing

    def play(self, audio: np.ndarray, sample_rate: int) -> None:
        """Play audio synchronously (blocks until done)."""
        with self._lock:
            self._playing = True
        try:
            logger.info("Playing audio (%.1fs)", len(audio) / sample_rate)
            sd.play(audio, samplerate=sample_rate)
            sd.wait()
            logger.info("Playback finished")
        finally:
            with self._lock:
                self._playing = False

    def stop(self) -> None:
        """Stop any ongoing playback."""
        sd.stop()
        with self._lock:
            self._playing = False
        logger.info("Playback stopped")
