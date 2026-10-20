#!/usr/bin/env bash
# macOS Standalone Application (.app) Builder using PyInstaller
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🏴‍☠️ Building Desktop Pirate .app for macOS..."

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
fi

.venv/bin/pip install PyQt6 Pillow pyinstaller

echo "Generating any missing sprite assets..."
.venv/bin/python3 sprite_generator.py
.venv/bin/python3 parrot_sprite_generator.py
.venv/bin/python3 piratess_sprite_generator.py
.venv/bin/python3 minion_sprite_generator.py

echo "Compiling .app bundle with PyInstaller..."
.venv/bin/pyinstaller \
    --name "DesktopPirate" \
    --windowed \
    --onedir \
    --osx-bundle-identifier "com.desktop.pirate" \
    --add-data "assets:assets" \
    --icon "assets/sprites/idle_right_0.png" \
    --clean \
    main.py

echo "Packaging dist/DesktopPirate.app into a zip archive..."
cd dist
zip -r DesktopPirate-macOS.zip DesktopPirate.app
cd ..

echo "✅ SUCCESS! Your macOS App is ready at:"
echo "   - dist/DesktopPirate.app"
echo "   - dist/DesktopPirate-macOS.zip"
