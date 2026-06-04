# engine.py - core AAC engine for behind-the-scenes, or should I say, behind-the-screens logic

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


import pygame as pg
from pygame.key import ScancodeWrapper

from .speak import speak
from .load_nodes import Button, LanguageTree, load_language_tree
from .constants import (
    SENTENCE_BAR_H,
    UI_PADDING,
    GRID_W,
    GRID_H,
    WN_W,
    WN_H
)

def _button_coord(screen_coords: tuple[int, int]) -> tuple[int, int] | None:
    """Get the corresponding button coordinates for a given screen coordinate.
    If there is no valid coordinate, return None."""

    min_x = UI_PADDING
    min_y = SENTENCE_BAR_H + UI_PADDING

    area_w = WN_W - min_x
    area_h = WN_H - min_y

    button_w = area_w / GRID_W
    button_h = area_h / GRID_H

    for by in range(GRID_H):
        for bx in range(GRID_W):
            screen_x = min_x + bx * button_w
            screen_y = min_y + by * button_h
            rect = pg.Rect(screen_x, screen_y, button_w - UI_PADDING, button_h - UI_PADDING)

            if rect.collidepoint(screen_coords):
                return bx, by

    return None

class AACEngine:
    """The engine class for the AAC talker (AAC = Augmentative and Alternative Communication)."""

    def __init__(self):
        self.sentence_bar: list[str] = []
        self.history: list[str] = []
        self.current_node: str = "HOME"
        self.tree: LanguageTree = load_language_tree()

    def _reset_history(self) -> None:
        self.current_node = "HOME"
        self.history.clear()

    def current_buttons(self) -> list[Button]:
        universal_node = self.tree.nodes.get("UNIVERSAL")
        node_buttons = self.tree[self.current_node].buttons

        if universal_node is None:
            return node_buttons

        return [*universal_node.buttons, *node_buttons]

    def _on_button_press(self, button: Button) -> None:
        # Update destination if the button has one
        if button.dest is not None:
            if isinstance(button.dest, int):
                # Relative offset - repeatedly set the current node to the last item in the history
                # until history is exhausted or the destination is reached
                to_remove = -button.dest
                for _ in range(to_remove):
                    if self.history:
                        self.current_node = self.history.pop()
            else:
                if button.dest != "HOME":
                    self.history.append(self.current_node)
                self.current_node = button.dest

        # Clear history if at HOME or history is exhausted
        if self.current_node == "HOME" or not self.history:
            self._reset_history()

        # Append word to sentence bar if the button has one
        if button.word is not None:
            speak(button.word.lower())  # normalise
            self.sentence_bar.append(button.word)

    def take_input(self, keys: ScancodeWrapper, events: list[pg.event.Event], dt_s: float) -> None:
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                button_coord = _button_coord(event.pos)

                if button_coord is not None:
                    for button in self.current_buttons():
                        if (button.coords[0] % GRID_W, button.coords[1] % GRID_H) == button_coord:
                            self._on_button_press(button)
                            break
