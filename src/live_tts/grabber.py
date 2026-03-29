"""Grab the currently selected text from the desktop."""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import time

logger = logging.getLogger(__name__)


class Grabber:
    """Captures the current text selection using system clipboard tools."""

    def __init__(self) -> None:
        self._session = os.environ.get("XDG_SESSION_TYPE", "x11")

    def grab(self) -> str:
        """Return the currently selected text, or empty string if nothing."""
        if self._session == "wayland":
            return self._grab_wayland()
        return self._grab_x11()

    def _grab_x11(self) -> str:
        """Grab selection on X11 using xclip."""
        # Save current clipboard
        try:
            saved = subprocess.run(
                ["xclip", "-selection", "clipboard", "-o"],
                capture_output=True,
                text=True,
                timeout=2,
            ).stdout
        except Exception:
            saved = ""

        # Copy current selection to clipboard via xdotool
        subprocess.run(
            ["xdotool", "key", "--clearmodifiers", "ctrl+c"],
            timeout=2,
            check=True,
        )
        time.sleep(0.1)

        # Read clipboard
        result = subprocess.run(
            ["xclip", "-selection", "clipboard", "-o"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        text = result.stdout.strip()

        # Restore previous clipboard content
        if saved:
            proc = subprocess.Popen(
                ["xclip", "-selection", "clipboard"],
                stdin=subprocess.PIPE,
            )
            proc.communicate(saved.encode())

        logger.debug("Grabbed text (%d chars): %s", len(text), text[:80])
        return text

    def _grab_wayland(self) -> str:
        """Grab selection on Wayland using wl-paste and wtype."""
        # Save current clipboard
        try:
            saved = subprocess.run(
                ["wl-paste"], capture_output=True, text=True, timeout=2
            ).stdout
        except Exception:
            saved = ""

        # Simulate Ctrl+C via wtype
        subprocess.run(
            ["wtype", "-M", "ctrl", "-P", "c", "-p", "c", "-m", "ctrl"],
            timeout=2,
            check=True,
        )
        time.sleep(0.1)

        # Read clipboard
        result = subprocess.run(
            ["wl-paste"], capture_output=True, text=True, timeout=2
        )
        text = result.stdout.strip()

        # Restore previous clipboard
        if saved:
            proc = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE)
            proc.communicate(saved.encode())

        logger.debug("Grabbed text (%d chars): %s", len(text), text[:80])
        return text
