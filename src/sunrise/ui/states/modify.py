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

from sunrise.core.bus import EventID
from sunrise.ui.states.base_states import State, StateID
from sunrise.ui.ui_buttons import CircularUIButton
from sunrise.core.constants import WN_W, WN_H, UI_PADDING, BORDER_WIDTH, ICON_SIZE

if TYPE_CHECKING:
    from sunrise.core.aac import AAC

class ModifyState(State):
    def __init__(self, aac_inst: AAC) -> None:
        super().__init__(aac_inst)
        self.popup_rect = pg.Rect(UI_PADDING, UI_PADDING, WN_W - UI_PADDING * 2, WN_H - UI_PADDING * 2)

        centre_x = WN_W - UI_PADDING - ICON_SIZE
        center_y = UI_PADDING + ICON_SIZE
        self.close_button = CircularUIButton(centre_x=centre_x, centre_y=center_y, r=ICON_SIZE // 2)

    def update(self, dt_s: float) -> None:
        pass

    def _handle_left_click(self, event: pg.event.Event) -> None:
        if self.close_button.check_click(event.pos):
            self.aac_inst.bus.emit(EventID.STATE_CHANGE, new_state=StateID.TALK)

    def take_input(self, keys: ScancodeWrapper, events: list[Event], dt_s: float) -> None:
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_left_click(event)

    def draw(self, screen: Surface) -> None:
        theme = self.aac_inst.get_current_theme()
        screen.fill(theme.bg_colour)
        pg.draw.rect(screen, theme.fg_colour, self.popup_rect, BORDER_WIDTH)

        rect = pg.Rect(0, 0, *self.aac_inst.assets.images.exit_icons[theme].get_size())
        rect.center = (self.close_button.centre_x, self.close_button.centre_y)
        screen.blit(self.aac_inst.assets.images.exit_icons[theme], rect)
