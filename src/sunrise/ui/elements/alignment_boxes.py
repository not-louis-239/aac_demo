# UI boxes

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

from sunrise.ui.elements.widget import DrawContext

from .widget import Widget

class _Box(Widget):
    # Generic base class to store attributes common to both `HBox`es and `VBox`es

    def __init__(self, *, padding: int = 0, gap: int = 0, children: list[Widget] | None = None) -> None:
        """Initialises a new box.
        padding = space between the box's edge and the first or last child
        gap     = space between children in the box"""
        super().__init__()
        self.padding = padding
        self.gap = gap

        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, child: Widget) -> None:
        self.children.append(child)
        child.parent = self

    def draw(self, surface: pg.Surface, ctx: DrawContext) -> None:
        for child in self.children:
            child.draw(surface, ctx)

class HBox(_Box):
    def preferred_size(self) -> tuple[int, int]:
        raise NotImplementedError  # TODO: implement abstract methods

    def layout(self, rect: pg.Rect) -> None:
        self.rect = rect

        x = rect.x + self.padding
        y = rect.y + self.padding
        height = rect.height - 2 * self.padding

        # measure fixed sizes
        total_fixed_width = 0
        flex_children = []

        for child in self.children:
            flex: int | None = getattr(child, "flex", None)
            if flex is not None:
                flex_children.append(child)
                continue
            w, _ = child.preferred_size()
            total_fixed_width += w

        total_gaps = self.gap * max(0, len(self.children) - 1)

        remaining = rect.width - 2 * self.padding - total_fixed_width - total_gaps

        # assign flex space
        total_flex = sum(getattr(c, "flex", 0) for c in flex_children)
        flex_widths = {}

        if total_flex > 0:
            for c in flex_children:
                flex_widths[c] = remaining * (c.flex / total_flex)

        # place children
        for i, child in enumerate(self.children):
            w, h = child.preferred_size()

            if child in flex_widths:
                w = int(flex_widths[child])

            child_rect = pg.Rect(x, y, w, height)
            child.layout(child_rect)

            x += w + self.gap

class VBox(_Box):
    pass  # TODO: implement abstract methods
