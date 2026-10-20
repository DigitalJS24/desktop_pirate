"""
Path resolution helper for development and PyInstaller standalone builds.
"""

import sys
import os

def get_base_dir():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def get_asset_path(*parts):
    return os.path.join(get_base_dir(), "assets", *parts)

