# app/core/paths.py
from pathlib import Path

# project_root = .../backend (folder that contains "app" and "media")
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # adjust if your layout differs

MEDIA_URL = "/media"                          # public URL prefix
MEDIA_DIR = PROJECT_ROOT / "media"     