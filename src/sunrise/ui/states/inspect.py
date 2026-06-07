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


from typing import TYPE_CHECKING

import pygame as pg
from pygame import Surface
from pygame.event import Event
from pygame.key import ScancodeWrapper

from .base_states import State
from sunrise.core.load_nodes import Button
from sunrise.core.constants import WN_W, WN_H, UI_PADDING

if TYPE_CHECKING:
    from sunrise.core.aac import AAC


class InspectState(State):
    def __init__(self, aac_inst: AAC) -> None:
        super().__init__(aac_inst)
        self.button: Button | None = None

    def _set_button(self, button: Button) -> None:
        self.button = button

    def update(self, dt_s: float) -> None:
        pass

    def take_input(self, keys: ScancodeWrapper, events: list[Event], dt_s: float) -> None:
        pass

    def draw(self, screen: Surface) -> None:
        screen.fill(self.aac_inst.get_current_theme().bg_colour)

        # Draw the popup background rect
        min_x, min_y = int(UI_PADDING), int(UI_PADDING)
        popup_w, popup_h = int(WN_W - 2 * UI_PADDING), int(WN_H - 2 * UI_PADDING)
        pg.draw.rect(screen, self.aac_inst.get_current_theme().fg_colour, (min_x, min_y, popup_w, popup_h), width=2)

        # Draw the 'x' button so users can actually get out!
