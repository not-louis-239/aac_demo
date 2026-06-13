# module for UI buttons
# these thingos are different from the other Button class as
# they are for UI menus, the other ones are for the AAC buttons

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


from abc import ABC, abstractmethod

import pygame as pg

from .widget import Widget


class UIButton(Widget, ABC):
    @abstractmethod
    def check_click(self, mouse_pos: tuple[int, int]) -> bool:
        raise NotImplementedError

class RectangularUIButton(UIButton):
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.Rect(x, y, w, h)

    def check_click(self, mouse_pos: tuple[int, int]) -> bool:
        return (
            self.x <= mouse_pos[0] <= self.x + self.w
            and self.y <= mouse_pos[1] <= self.y + self.h
        )

class CircularUIButton(UIButton):
    def __init__(self, centre_x: int, centre_y: int, r: int) -> None:
        self.centre_x = centre_x
        self.centre_y = centre_y
        self.r = r

    def check_click(self, mouse_pos: tuple[int, int]) -> bool:
        return (mouse_pos[0] - self.centre_x) ** 2 + (mouse_pos[1] - self.centre_y) ** 2 <= self.r ** 2
