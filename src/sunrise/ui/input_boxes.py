# module for reusable input boxes

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

import pygame as pg
from sunrise.core.constants import UI_PADDING
from sunrise.core.custom_types import Colour

class InputBox:
    def __init__(self, x: int, y: int, w: int, h: int, font: pg.font.Font) -> None:
        self.rect = pg.Rect(x, y, w, h)
        self.text = ""
        self.active = False
        self.font = font  # needed so that it can auto-adjust text width while drawing



    def handle_click(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key not in (pg.K_RETURN, pg.K_ESCAPE, pg.K_TAB):
                    # Append character
                    self.text += event.unicode

    def draw(
            self, screen: pg.Surface,
            bg_active_colour: Colour, bg_inactive_colour: Colour,
            fg_colour: Colour, border_colour: Colour
        ) -> None:
        # Passing the colours into the method instead of
        # as attributes because these suckers shouldn't really need to know
        # what colour they are, and it makes multiple themes harder
        # because then you'd need to change the colour of the `InputBox`es
        # every time you wanted to change theme

        # Draw the background and border
        bg_colour = bg_active_colour if self.active else bg_inactive_colour
        pg.draw.rect(screen, bg_colour, self.rect)

        # Text
        last_127_chars = self.text[-127:]  # drawing only last 127 characters for performance
        text_surf = self.font.render(last_127_chars, True, fg_colour)
        text_visual_width = self.rect.width - 2 * UI_PADDING
        source_rect = pg.Rect(
            max(0, text_surf.get_width() - text_visual_width),
            0,
            min(text_visual_width, text_surf.get_width()),
            text_surf.get_height()
        )

        screen.blit(text_surf, (self.rect.x + UI_PADDING, self.rect.y), source_rect)

        # Border
        pg.draw.rect(screen, border_colour, self.rect, width=2)
