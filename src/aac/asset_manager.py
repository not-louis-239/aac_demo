from .paths import FONTS_DIR
from pathlib import Path

class Fonts:
    def __init__(self) -> None:
        self.button_font: Path = FONTS_DIR / "ComicNeue-Bold.ttf"
        self.ui_font: Path = FONTS_DIR / "AtkinsonHyperlegible-Regular.ttf"

class Images:
    def __init__(self) -> None:
        pass  # more images will be added when needed

class Assets:
    def __init__(self) -> None:
        self.fonts = Fonts()
        self.images = Images()
