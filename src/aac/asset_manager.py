from pathlib import Path

import pygame as pg

from aac.paths import FONTS_DIR


class Fonts:
    def __init__(self) -> None:
        self.button_font: Path = FONTS_DIR / "ComicNeue-Bold.ttf"
        self.ui_font: Path = FONTS_DIR / "AtkinsonHyperlegible-Regular.ttf"

class Images:
    def __init__(self) -> None:
        # {relative_fp, pg.Surface} pairs
        self.image_cache: dict[str, pg.Surface] = {}

class Assets:
    def __init__(self) -> None:
        self.fonts = Fonts()
        self.images = Images()
