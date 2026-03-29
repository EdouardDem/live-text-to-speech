#!/bin/bash
set -euo pipefail

# Install system dependencies
sudo apt install -y libportaudio2 xdotool xclip

# Create virtual environment if needed
if [ ! -d .venv ]; then
    python3 -m venv .venv
fi

# Activate and install
source .venv/bin/activate
pip install -e .
