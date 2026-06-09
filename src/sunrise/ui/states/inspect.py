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

from crystallinium.text_utils import draw_text

from .base_states import State, StateID
from ..ui_buttons import CircularUIButton
from sunrise.core.bus import EventID
from sunrise.ui.utils import crop_text_to_fit
from sunrise.core.load_nodes import Button
from sunrise.core.constants import WN_W, WN_H, UI_PADDING, ICON_SIZE, UI_MARGIN

if TYPE_CHECKING:
    from sunrise.core.aac import AAC


class InspectState(State):
    def __init__(self, aac_inst: AAC) -> None:
        super().__init__(aac_inst)
        self.button: Button | None = None  # the button that `self` is currently inspecting
        self.node_label: str | None = None
        self.aac_inst.bus.subscribe(EventID.SET_BUTTON, self.set_button_and_node)

        min_x, min_y = int(UI_PADDING), int(UI_PADDING)
        popup_w, popup_h = int(WN_W - 2 * UI_PADDING), int(WN_H - 2 * UI_PADDING)
        self.popup_rect = pg.Rect(min_x, min_y, popup_w, popup_h)

        close_button_radius = ICON_SIZE // 2
        close_button_centre_x = int(min_x + popup_w - close_button_radius - UI_PADDING)
        close_button_centre_y = int(min_y + close_button_radius + UI_PADDING)
        self.close_button = CircularUIButton(centre_x=close_button_centre_x, centre_y=close_button_centre_y, r=close_button_radius)

        self.title_font = pg.font.Font(self.aac_inst.assets.fonts.ui_font, 35)

    def set_button_and_node(self, button: Button, node_label: str) -> None:
        self.button = button
        self.node_label = node_label

    def update(self, dt_s: float) -> None:
        pass

    def take_input(self, keys: ScancodeWrapper, events: list[Event], dt_s: float) -> None:
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.close_button.check_click(*event.pos):
                    self.aac_inst.bus.emit(EventID.STATE_CHANGE, new_state=StateID.TALK)

    def draw(self, screen: Surface) -> None:
        theme = self.aac_inst.get_current_theme()
        screen.fill(theme.bg_colour)

        if not self.button:
            return

        # Draw the popup background rect
        pg.draw.rect(screen, theme.fg_colour, self.popup_rect, width=2)

        # Draw the 'x' button so users can actually get out!
        topleft = (self.popup_rect.right - 2 * self.close_button.r - UI_PADDING, self.popup_rect.top + UI_PADDING)
        screen.blit(self.aac_inst.assets.images.exit_icons[theme], topleft)

        # Draw the popup text
        text_left, text_top = self.popup_rect.topleft[0] + UI_PADDING, self.popup_rect.topleft[1] + UI_PADDING
        text = f"Button '{self.button.label}' in Node '{self.node_label}' at {self.button.coords}"
        text_max_width = int(self.popup_rect.width - 2 * self.close_button.r - 3 * UI_PADDING)
        text_cropped = crop_text_to_fit(text, self.title_font, text_max_width)

        text_surf = self.title_font.render(text_cropped, True, theme.fg_colour)
        screen.blit(text_surf, (text_left, text_top))

        base_x, base_y = (UI_PADDING + UI_MARGIN, int(WN_H * 0.15))
        value_offset = 150

        def draw_key_value_pair(k: object, v: object, pos: tuple[int, int]) -> None:
            px, py = pos

            draw_text(
                surface=screen, pos=(px, py),
                horiz_align='left', vert_align='top',
                font_family=self.title_font, text=str(k),
                colour=theme.fg_colour
            )

            if v is not None:
                v_str = str(v)
                v_col = theme.fg_colour
            else:
                v_str = "n/a"
                v_col = (*theme.fg_colour, 127)

            draw_text(
                surface=screen, pos=(px + value_offset, py),
                horiz_align='left', vert_align='top',
                font_family=self.title_font, text=v_str,
                colour=v_col
            )

        for i, (k, v) in enumerate({
            "word:": self.button.word,
            "dest:": self.button.dest,
            "func:": self.button.func,
            "image:": self.button.img,
            "type:": self.button.type,
        }.items()):
            pos = base_x, base_y + i * UI_MARGIN
            draw_key_value_pair(k=k, v=v, pos=pos)
