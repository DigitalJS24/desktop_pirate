#!/usr/bin/env bash
# macOS Launcher for Desktop Pirate
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🏴‍☠️ Starting Desktop Pirate on macOS..."

# Create venv if not present
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install PyQt6 Pillow
fi

# Run application in background
nohup .venv/bin/python3 main.py >/dev/null 2>&1 &
echo "Desktop Pirate is running on your Mac desktop!"
