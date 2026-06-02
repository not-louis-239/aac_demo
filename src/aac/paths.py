from pathlib import Path

try:
    ROOT_DIR = next(p for p in Path(__file__).resolve().parents if (p / ".git").exists())
except StopIteration:
    raise RuntimeError("Could not find root directory.")

ASSETS_DIR = ROOT_DIR / "assets"

FONTS_DIR = ASSETS_DIR / "fonts"
IMAGES_DIR = ASSETS_DIR / "images"

NODES_FILE = ROOT_DIR / "tree" / "nodes.json"
