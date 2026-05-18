# tg-launch-alert

A **tiny** command‑line tool written in Python that fetches the latest messages from a Telegram bot (or channel) and prints any launch alerts it finds.

## Features
- Minimal dependencies (`requests` only).
- One‑click run via `python tg_launch_alert.py`.
- Configurable via environment variables.

## Installation
```bash
# Clone the repo (or copy the files)
git clone https://github.com/yourusername/tg-launch-alert.git
cd tg-launch-alert

# Install the only required package
pip install -r <(echo "requests")
```

## Usage
Set the required environment variables and run the script:
```bash
export TG_BOT_TOKEN="123456:ABCDEF..."
export TG_CHAT_ID="-1001234567890"   # ID of the chat/channel to monitor
python tg_launch_alert.py
```
The script will fetch the last 20 messages and print any that contain the keyword `launch` (case‑insensitive).

## Customisation
- Change the `KEYWORD` constant in the script to look for a different trigger word.
- Adjust the `MESSAGE_LIMIT` constant to fetch more or fewer messages.

## License
This is a tiny demo project; feel free to copy, modify, and share.
