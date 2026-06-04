# module for rendering the AAC user interface
# repo at: https://github.com/not-louis-239/aac_demo
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


from typing import TYPE_CHECKING

import pygame as pg

from crystallinium.text_utils import draw_text

from aac.paths import IMAGES_DIR
from aac.asset_manager import Images
from aac.load_nodes import Button
from aac.constants import (
    WN_W, WN_H,
    GRID_W, GRID_H,
    SENTENCE_BAR_H,
    BUTTON_BORDER_WIDTH,
    BUTTON_FONT_SIZE,
    UI_PADDING,
    THEMES
)

if TYPE_CHECKING:
    from aac.aac_main import AAC

def retrieve_img(img: Images, rel_path: str) -> pg.Surface:
    """Relative path is relative to assets/images,
    e.g. './food/apple.png'"""

    if rel_path not in img.image_cache:
        clean_rel_path = rel_path.lstrip("./") if rel_path.startswith("./") else rel_path
        path = IMAGES_DIR / clean_rel_path
        img.image_cache[rel_path] = pg.image.load(path).convert_alpha()

    return img.image_cache[rel_path]

class Renderer:
    def __init__(self, aac_inst: AAC):
        self.aac_inst = aac_inst
        self.theme_idx: int = 0
        self.sentence_bar_font: pg.font.Font = pg.font.Font(self.aac_inst.assets.fonts.ui_font, int(SENTENCE_BAR_H * 0.5))

    def _calculate_button_rect(self, button: Button) -> pg.Rect:
        bx, by = button.coords
        bx, by = bx % GRID_W, by % GRID_H  # normalise negative coordinates

        min_x = UI_PADDING
        min_y = SENTENCE_BAR_H + UI_PADDING

        # The size of the button area, minus the left/top margins
        area_w = WN_W - min_x
        area_h = WN_H - min_y

        button_w = area_w / GRID_W
        button_h = area_h / GRID_H

        screen_x = min_x + bx * button_w
        screen_y = min_y + by * button_h
        return pg.Rect(screen_x, screen_y, button_w - UI_PADDING, button_h - UI_PADDING)

    def _draw_button(self, screen: pg.Surface, button: Button) -> None:
        # Draw button rect
        rect = self._calculate_button_rect(button)

        theme = THEMES[self.theme_idx]
        colour = theme.fitzgerald_theme.get(button.type) or theme.fitzgerald_theme["system"]

        # Draw the actual rect first
        pg.draw.rect(screen, colour, rect)
        # Now border
        pg.draw.rect(screen, theme.fg_colour, rect, BUTTON_BORDER_WIDTH)

        # Now the text
        text_centre_x = rect.centerx
        text_centre_y = rect.top + rect.height // 10

        draw_text(
            surface=screen, pos=(text_centre_x, text_centre_y),
            horiz_align="centre", vert_align="top", colour=theme.fg_colour,
            text=str(button.label), font_family=(self.aac_inst.assets.fonts.button_font, 15)
        )

    def draw(self, screen: pg.Surface) -> None:
        theme = THEMES[self.theme_idx]
        screen.fill((theme.bg_colour))

        # Draw buttons
        eng = self.aac_inst.engine
        for button in eng.current_buttons():
            self._draw_button(screen=screen, button=button)

        # Now draw the sentence bar line
        pg.draw.line(screen, theme.fg_colour, (0, SENTENCE_BAR_H), (WN_W, SENTENCE_BAR_H), 2)
        # Draw the sentence bar text
        sentence_bar_text = " ".join(self.aac_inst.engine.sentence_bar)

        # rendering a maximum of 255 characters for performance
        max_width = WN_W - 2 * UI_PADDING
        text_surf = self.sentence_bar_font.render(sentence_bar_text[:255], True, theme.fg_colour)
        if (big_width := text_surf.get_width()) > max_width:
            excess = big_width - max_width
            crop_rect = pg.Rect(excess, 0, max_width, text_surf.get_height())
            text_surf = text_surf.subsurface(crop_rect)

        screen.blit(text_surf, (UI_PADDING, UI_PADDING))
