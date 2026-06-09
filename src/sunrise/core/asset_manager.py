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

from sunrise.ui.utils import make_tinted_surface
from sunrise.core.custom_types import Colour
from sunrise.core.paths import FONTS_DIR, UI_IMAGES_DIR
from sunrise.core.constants import THEMES, ICON_SIZE, Theme


class Fonts:
    def __init__(self) -> None:
        self.button_font: Path = FONTS_DIR / "ComicNeue-Bold.ttf"
        self.ui_font: Path = FONTS_DIR / "AtkinsonHyperlegible-Regular.ttf"


class Images:
    def __init__(self) -> None:
        # {relative_fp, pg.Surface} pairs
        self.cache: dict[str, pg.Surface] = {}

        # {theme colour: coloured icon}
        self.exit_icons: dict[Theme, pg.Surface] = {}
        self.proceed_icons: dict[Theme, pg.Surface] = {}

        self.init_coloured_icons()

    def init_coloured_icons(self, themes: list[Theme] = THEMES) -> None:
        # Load icons
        exit_icon = pg.transform.scale(
            pg.image.load(UI_IMAGES_DIR / "exit.png").convert_alpha(), (ICON_SIZE, ICON_SIZE)
        )
        proceed_icon = pg.transform.scale(
            pg.image.load(UI_IMAGES_DIR / "proceed.png").convert_alpha(), (ICON_SIZE, ICON_SIZE)
        )

        # Then make the coloured copies for each theme
        for theme in themes:
            exit_colour = theme.err_colour
            self.exit_icons[theme] = make_tinted_surface(exit_icon, exit_colour)
            proceed_colour = theme.ok_colour
            self.proceed_icons[theme] = make_tinted_surface(proceed_icon, proceed_colour)

class Assets:
    def __init__(self) -> None:
        self.fonts = Fonts()
        self.images = Images()
