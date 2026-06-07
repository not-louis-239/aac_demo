# asset_manager.py - Asset Manager
# repo at: https://github.com/not-louis-239/sunrise-aac
# Copyright (C) 2026 Louis Masarei-Boulton <243234869+not-louis-239@users.noreply.github.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from pathlib import Path

import pygame as pg

from sunrise.core.paths import FONTS_DIR


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
