# icons

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

from .widget import Widget, DrawContext, LayoutContext

class Icon(Widget):
    def __init__(self, img_path: Path, size: tuple[int, int]) -> None:
        super().__init__()
        self.img_path = img_path
        self.size = size
        self._cached: pg.Surface | None = None
        self._refresh_cache()

    def _refresh_cache(self) -> None:
        if self._cached is None or self._cached.get_size() != self.size:
            self._cached = pg.image.load(str(self.img_path)).convert_alpha()
            self._cached = pg.transform.scale(self._cached, self.size)

    def preferred_size(self, ctx: LayoutContext) -> tuple[int, int]:
        return self.size

    def layout(self, rect: pg.Rect) -> None:
        self.rect = pg.Rect(0, 0, *self.size)
        self.rect.center = rect.center

    def draw(self, surface: pg.Surface, ctx: DrawContext) -> None:
        self._refresh_cache()
        assert self._cached is not None
        surface.blit(self._cached, self.rect.topleft)
