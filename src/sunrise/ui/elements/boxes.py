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

class HBox(_Box):
    pass  # TODO: implement abstract methods

class VBox(_Box):
    pass  # TODO: implement abstract methods
