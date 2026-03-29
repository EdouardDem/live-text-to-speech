"""Global hotkey listener."""

from __future__ import annotations

import logging
from typing import Callable

from pynput import keyboard

logger = logging.getLogger(__name__)


class HotkeyListener:
    """Listens for a global hotkey combination."""

    def __init__(self, hotkey: str, callback: Callable[[], None]) -> None:
        self._hotkey_str = hotkey
        self._callback = callback
        self._listener: keyboard.Listener | None = None
        self._hotkey = keyboard.HotKey(
            keyboard.HotKey.parse(hotkey), self._on_activate
        )

    def _on_activate(self) -> None:
        logger.debug("Hotkey activated: %s", self._hotkey_str)
        self._callback()

    def _for_canonical(self, f: Callable) -> Callable:
        """Normalize key events through the listener's canonical mapping."""
        return lambda k: f(self._listener.canonical(k))

    def start(self) -> None:
        logger.info("Listening for hotkey: %s", self._hotkey_str)
        self._listener = keyboard.Listener(
            on_press=self._for_canonical(self._hotkey.press),
            on_release=self._for_canonical(self._hotkey.release),
        )
        self._listener.start()

    def stop(self) -> None:
        if self._listener:
            self._listener.stop()
            self._listener = None
