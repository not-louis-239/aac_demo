# labels

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


class Label:
    def __init__(self, font: pg.font.Font, text: str = "") -> None:
        self.font = font
        self.text = text
        self.rect = pg.Rect(0, 0, *self.font.size(text))

    def _sync_size(self) -> None:
        self.rect.width = self.font.size(self.text)[0]

    def set_text(self, text: str) -> None:
        self.text = text
        self._sync_size()

    def draw(self, screen: pg.Surface, colour: Colour | AColour, pos: tuple[int, int]) -> None:
        font_surf = self.font.render(self.text, True, colour)
        if len(colour) == 4:
            font_surf.set_alpha(colour[3])
        screen.blit(font_surf, pos)
