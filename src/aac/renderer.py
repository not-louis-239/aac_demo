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
from pathlib import Path
import sys

import pygame as pg

from crystallinium.text_utils import draw_text

from aac.terminal_formatting import COL_END, COL_BOLD, COL_WARN
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
    THEMES,
    IMAGE_SIZE
)

if TYPE_CHECKING:
    from aac.aac_main import AAC

# set of paths for which a warning has already been printed
# to prevent spamming warnings for the same path
_warned_paths: set[str] = set()

def resize_surface_fit(surface: pg.Surface, max_size: int) -> pg.Surface:
    """Resizes a surface to be as large as possible, ensuring neither width nor height
    exceeds max_size, while perfectly preserving the aspect ratio."""

    target_rect = pg.Rect(0, 0, max_size, max_size)
    current_rect = surface.get_rect()
    fitted_rect = current_rect.fit(target_rect)
    return pg.transform.smoothscale(surface, (fitted_rect.width, fitted_rect.height))

def retrieve_img(img: Images, rel_path: str | None) -> pg.Surface | None:
    """Load an image from an images manager and
    a relative path.
    Relative path is relative to assets/images,
    e.g. './food/apple.png'.
    If the file is not accessible (e.g. doesn't exist, permission denied),
    return None and log an error to stderr."""

    if rel_path is None:
        return None

    if rel_path not in _warned_paths and Path(rel_path).is_dir():
        _warned_paths.add(rel_path)
        print(f"warning: cannot load image: expected image, got directory: '{rel_path}'", file=sys.stderr)
        return None

    try:
        if rel_path not in img.image_cache:
            clean_rel_path = rel_path.lstrip("./") if rel_path.startswith("./") else rel_path
            path = IMAGES_DIR / clean_rel_path
            img_loaded = pg.image.load(path).convert_alpha()

            # scale the image so it fits within the buttons
            img_loaded = resize_surface_fit(img_loaded, IMAGE_SIZE)
            img.image_cache[rel_path] = img_loaded

        return img.image_cache[rel_path]
    except FileNotFoundError:
        if rel_path not in _warned_paths:
            print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: cannot load image: no such file: {COL_WARN}'{rel_path}'{COL_END}", file=sys.stderr)
            _warned_paths.add(rel_path)
        return None
    except PermissionError:
        if rel_path not in _warned_paths:
            print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: cannot load image: read permission denied: {COL_WARN}'{rel_path}'{COL_END}", file=sys.stderr)
            _warned_paths.add(rel_path)
        return None
    except Exception as e:
        if rel_path not in _warned_paths:
            print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: cannot load image: {COL_WARN}'{rel_path}'{COL_END} - unexpected error: {e}", file=sys.stderr)
            _warned_paths.add(rel_path)
        return None

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

        # Now the image
        img = retrieve_img(img=self.aac_inst.assets.images, rel_path=str(button.img) if button.img is not None else None)
        if img is not None:
            img_rect = img.get_rect()
            img_rect.center = (rect.centerx, int(rect.centery + BUTTON_FONT_SIZE // 2))
            screen.blit(img, img_rect)

        # Now the text
        text_centre_x = rect.centerx
        if not img:
            text_y = rect.centery  # no image -> print text in centre of the rect
        else:
            text_y = rect.top

        draw_text(
            surface=screen, pos=(text_centre_x, text_y),
            horiz_align="centre", vert_align="top" if img else "centre", colour=theme.fg_colour,
            text=str(button.label), font_family=(self.aac_inst.assets.fonts.button_font, int(BUTTON_FONT_SIZE))
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

        # rendering only the last 255 characters for performance
        # this is arbitrary but we expect here that a little kid might
        # spam the buttons on the AAC thousands of times
        # if not optimised, this could cause severe lag
        max_width = WN_W - 2 * UI_PADDING
        text_surf = self.sentence_bar_font.render(sentence_bar_text[-255:], True, theme.fg_colour)
        if (big_width := text_surf.get_width()) > max_width:
            excess = big_width - max_width
            crop_rect = pg.Rect(excess, 0, max_width, text_surf.get_height())
            text_surf = text_surf.subsurface(crop_rect)

        screen.blit(text_surf, (UI_PADDING, UI_PADDING))
