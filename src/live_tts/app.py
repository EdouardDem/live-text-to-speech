"""Main application orchestrator."""

from __future__ import annotations

import logging
import signal
import threading

from .config import Config
from .grabber import Grabber
from .hotkey import HotkeyListener
from .player import Player
from .synthesizer import Synthesizer
from .tray import TrayIcon, STATE_IDLE, STATE_GRABBING, STATE_SYNTHESIZING, STATE_PLAYING

logger = logging.getLogger(__name__)


class App:
    """Wires all components together."""

    def __init__(self, config: Config, use_tray: bool = True) -> None:
        self._config = config
        self._use_tray = use_tray
        self._lock = threading.Lock()
        self._busy = False

        self._grabber = Grabber()
        self._synthesizer = Synthesizer(config)
        self._player = Player()
        self._hotkey = HotkeyListener(config.hotkey, self._on_trigger)
        self._tray: TrayIcon | None = None

    def run(self) -> None:
        logger.info("Starting live-tts (hotkey=%s, voice=%s)", self._config.hotkey, self._config.voice)

        self._hotkey.start()

        if self._use_tray:
            self._tray = TrayIcon(
                on_trigger=self._on_trigger,
                on_quit=self._shutdown,
            )
            self._tray.start()  # blocks
        else:
            stop_event = threading.Event()

            def _handle_signal(signum, frame):
                logger.info("Signal %s received, shutting down", signum)
                stop_event.set()

            signal.signal(signal.SIGINT, _handle_signal)
            signal.signal(signal.SIGTERM, _handle_signal)
            logger.info("Running headless (no tray). Press Ctrl+C to quit.")
            stop_event.wait()

        self._shutdown()

    def _shutdown(self) -> None:
        logger.info("Shutting down")
        self._player.stop()
        self._hotkey.stop()
        self._synthesizer.close()
        if self._tray:
            self._tray.stop()

    def _on_trigger(self) -> None:
        """Called when the hotkey is pressed or tray menu is clicked."""
        with self._lock:
            if self._busy:
                # If already playing, stop playback
                if self._player.playing:
                    self._player.stop()
                    return
                logger.debug("Already processing, ignoring trigger")
                return
            self._busy = True

        thread = threading.Thread(target=self._process, daemon=True)
        thread.start()

    def _process(self) -> None:
        """Grab text, synthesize speech, play audio."""
        try:
            # Grab selected text
            self._set_state(STATE_GRABBING)
            text = self._grabber.grab()
            if not text:
                logger.warning("No text selected")
                return

            # Synthesize
            self._set_state(STATE_SYNTHESIZING)
            audio, sample_rate = self._synthesizer.synthesize(text)

            # Play
            self._set_state(STATE_PLAYING)
            self._player.play(audio, sample_rate)

        except Exception:
            logger.exception("Error during TTS processing")
        finally:
            self._set_state(STATE_IDLE)
            with self._lock:
                self._busy = False

    def _set_state(self, state: str) -> None:
        logger.debug("State -> %s", state)
        if self._tray:
            self._tray.set_state(state)
