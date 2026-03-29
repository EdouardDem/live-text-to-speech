# Live Text-to-Speech

A lightweight Linux daemon that reads aloud any selected text, powered by
[Mistral Voxtral 4B TTS](https://huggingface.co/mistralai/Voxtral-4B-TTS-2603).

## How it works

1. Select any text on your desktop.
2. Press a global hotkey (default **Ctrl+Shift+A**).
3. The selected text is sent to a local Voxtral server for speech synthesis.
4. The generated audio is played back through your speakers.
5. Press the hotkey again during playback to stop it.

A system-tray icon provides visual feedback:

| Color  | State        |
| ------ | ------------ |
| Grey   | Idle         |
| Blue   | Grabbing     |
| Orange | Synthesizing |
| Green  | Playing      |

## Prerequisites

A running [vLLM](https://docs.vllm.ai/) server with Voxtral is required (GPU with >= 16 GB VRAM).

### Option A: Docker (recommended)

```bash
docker compose up -d

# Follow logs (first launch downloads the model ~8 GB)
docker compose logs -f
```

If the model requires a HuggingFace token:

```bash
HF_TOKEN=hf_xxx docker compose up -d
```

### Option B: Manual

```bash
# Install vLLM
pip install -U vllm
pip install git+https://github.com/vllm-project/vllm-omni.git --upgrade

# Start the server
vllm serve mistralai/Voxtral-4B-TTS-2603 --omni
```

## Installation

### Installation script

```bash
./install.sh
```

### Uninstallation script

```bash
./uninstall.sh
```

### Step by step installation

#### 1. System packages (Debian / Ubuntu)

```bash
# Audio playback
sudo apt install libportaudio2

# Text selection capture (X11)
sudo apt install xdotool xclip

# Text selection capture (Wayland — instead of xdotool/xclip)
# sudo apt install wl-clipboard wtype
```

#### 2. Python

Python >= 3.10 is required. A virtual environment is recommended:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install

```bash
pip install -e .
```

## Usage

```bash
# Run with system tray icon (default)
live-tts

# Run headless (no tray, Ctrl+C to quit)
live-tts --no-tray

# Override the hotkey
live-tts --hotkey '<ctrl>+<shift>+s'

# Choose a different voice
live-tts --voice casual_female

# Point to a remote server
live-tts --server-url http://192.168.1.10:8000

# Verbose logging
live-tts --verbose
```

You can also run it as a module:

```bash
python -m live_tts
```

## Configuration

If you want a persistent configuration, copy the example config and edit the config file:

```bash
mkdir -p ~/.config/live-tts
cp config.yaml ~/.config/live-tts/config.yaml
```

Settings can also be set via CLI flags (see `live-tts --help`).

| Key               | Default                          | Description                   |
| ----------------- | -------------------------------- | ----------------------------- |
| `hotkey`          | `<ctrl>+<shift>+a`              | Global hotkey (pynput format) |
| `server_url`      | `http://localhost:8000`          | vLLM server URL               |
| `model_name`      | `mistralai/Voxtral-4B-TTS-2603` | Model identifier              |
| `voice`           | `fr_male`                        | Voice preset (see below)      |
| `response_format` | `wav`                            | Audio format                  |

## Available voices

Voxtral ships with 20 preset voices:

| Voice             | Language   |
| ----------------- | ---------- |
| `casual_female`   | English    |
| `casual_male`     | English    |
| `cheerful_female` | English    |
| `neutral_female`  | English    |
| `neutral_male`    | English    |
| `fr_male`         | French     |
| `fr_female`       | French     |
| `es_male`         | Spanish    |
| `es_female`       | Spanish    |
| `de_male`         | German     |
| `de_female`       | German     |
| `it_male`         | Italian    |
| `it_female`       | Italian    |
| `pt_male`         | Portuguese |
| `pt_female`       | Portuguese |
| `nl_male`         | Dutch      |
| `nl_female`       | Dutch      |
| `ar_male`         | Arabic     |
| `hi_male`         | Hindi      |
| `hi_female`       | Hindi      |

## Supported languages

English, French, Spanish, German, Italian, Portuguese, Dutch, Arabic, Hindi.

## License

See [LICENSE](LICENSE).
