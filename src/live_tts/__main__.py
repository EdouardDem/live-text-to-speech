"""CLI entry point for live-tts."""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import sys

from .config import Config, VOICES


def _check_deps() -> None:
    """Check that required system tools are available."""
    session = os.environ.get("XDG_SESSION_TYPE", "x11")
    if session == "wayland":
        required = ["wl-copy", "wl-paste", "wtype"]
    else:
        required = ["xclip", "xdotool"]
    missing = [cmd for cmd in required if not shutil.which(cmd)]
    if missing:
        print(
            f"Missing system dependencies: {', '.join(missing)}\n"
            f"Install them with: sudo apt install {' '.join(missing)}",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="live-tts",
        description="Live text-to-speech daemon using Mistral Voxtral",
    )
    parser.add_argument(
        "--config", type=str, default=None, help="Path to config YAML file"
    )
    parser.add_argument("--hotkey", type=str, help="Hotkey combo (pynput format)")
    parser.add_argument("--server-url", type=str, help="vLLM server URL")
    parser.add_argument("--voice", type=str, choices=VOICES, help="Voice preset")
    parser.add_argument("--no-tray", action="store_true", help="Run without tray icon")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    _check_deps()

    from pathlib import Path

    cfg = Config.load(Path(args.config) if args.config else None)

    if args.hotkey:
        cfg.hotkey = args.hotkey
    if args.server_url:
        cfg.server_url = args.server_url
    if args.voice:
        cfg.voice = args.voice

    from .app import App

    app = App(cfg, use_tray=not args.no_tray)
    app.run()


if __name__ == "__main__":
    main()
