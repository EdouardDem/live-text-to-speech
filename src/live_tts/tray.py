"""System tray icon."""

from __future__ import annotations

import logging
from typing import Callable

from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

logger = logging.getLogger(__name__)

# States and their colors
STATE_IDLE = "idle"
STATE_GRABBING = "grabbing"
STATE_SYNTHESIZING = "synthesizing"
STATE_PLAYING = "playing"

_COLORS = {
    STATE_IDLE: "#888888",
    STATE_GRABBING: "#3498db",
    STATE_SYNTHESIZING: "#f39c12",
    STATE_PLAYING: "#2ecc71",
}


class TrayIcon:
    """System tray icon with state feedback."""

    def __init__(
        self,
        on_trigger: Callable[[], None],
        on_quit: Callable[[], None],
    ) -> None:
        self._on_trigger = on_trigger
        self._on_quit = on_quit
        self._state = STATE_IDLE
        self._icon = Icon(
            "live-tts",
            icon=self._make_icon(STATE_IDLE),
            title="Live TTS (idle)",
            menu=Menu(
                MenuItem("Read selection", lambda: self._on_trigger()),
                MenuItem("Quit", lambda: self._on_quit()),
            ),
        )

    def set_state(self, state: str) -> None:
        self._state = state
        self._icon.icon = self._make_icon(state)
        self._icon.title = f"Live TTS ({state})"

    def _make_icon(self, state: str) -> Image.Image:
        """Generate a 64x64 icon with a colored circle."""
        color = _COLORS.get(state, _COLORS[STATE_IDLE])
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 4, 60, 60], fill=color)
        # Inner indicator for active states
        if state in (STATE_SYNTHESIZING, STATE_PLAYING):
            draw.ellipse([20, 20, 44, 44], fill="white")
        return img

    def start(self) -> None:
        """Start the tray icon (blocking)."""
        logger.info("Starting system tray icon")
        self._icon.run()

    def stop(self) -> None:
        self._icon.stop()
