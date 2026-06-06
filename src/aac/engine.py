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


import sys
from typing import Any, Callable
from pathlib import Path

import pygame as pg
from pygame.key import ScancodeWrapper

from .terminal_formatting import COL_ERR, COL_WARN, COL_END, COL_BOLD
from .speak import speak, stop_speaking as _stop_speaking
from .load_nodes import Button, LanguageTree, load_language_tree, save_language_tree
from .constants import (
    SENTENCE_BAR_H,
    UI_PADDING,
    GRID_W,
    GRID_H,
    WN_W,
    WN_H
)

_warned_nodes: set[str] = set()
_warned_funcs: set[str] = set()

def _read_positive_int_coord(max_val: int, *, prompt: str) -> int:
    """Read a positive integer coordinate from user input, ensuring it falls from 0 - max_val (inclusive)."""
    while True:
        try:
            value = int(input(prompt).strip())
            if 0 <= value <= max_val:
                return value
            print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: expected a positive integer between 0 and {max_val}", file=sys.stderr)
        except ValueError:
            print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: invalid input, please enter a positive integer", file=sys.stderr)

def _button_coord(screen_coords: tuple[int, int]) -> tuple[int, int] | None:
    """Get the corresponding button coordinates for a given screen coordinate.
    If there is no valid coordinate, return None."""

    x, y = screen_coords

    min_x = UI_PADDING
    min_y = SENTENCE_BAR_H + UI_PADDING

    # Calculate individual button dimensions
    area_w = WN_W - min_x
    area_h = WN_H - min_y
    button_w = area_w / GRID_W
    button_h = area_h / GRID_H

    # Is the click inside the grid at all?
    if x < min_x or x >= WN_W or y < min_y or y >= WN_H:
        return None

    # Derive the grid index directly using integer division
    bx = int((x - min_x) // button_w)
    by = int((y - min_y) // button_h)

    # Gaps between buttons where a click shouldn't trigger anything.
    button_start_x = min_x + bx * button_w
    button_start_y = min_y + by * button_h

    # Check if the click fell into the padding gap at the right or bottom of the button
    if (x >= button_start_x + (button_w - UI_PADDING)) or (y >= button_start_y + (button_h - UI_PADDING)):
        return None

    # Safety check to ensure floating-point rounding didn't push us out of bounds
    if 0 <= bx < GRID_W and 0 <= by < GRID_H:
        return bx, by

    return None


def _get_button_at_pos(buttons: list[Button], coords: tuple[int, int]) -> Button | None:
    """Get the button at a specific grid position in a list of buttons.
    If no such button exists there in the list, return None."""

    for button in buttons:
        if (button.coords[0] % GRID_W, button.coords[1] % GRID_H) == coords:
            return button
    return None


class AACEngine:
    """The engine class for the AAC talker (AAC = Augmentative and Alternative Communication)."""

    FUNC_REGISTRY: dict[str, Callable[[Any], None]] = {}

    @classmethod
    def register(cls, func_alias: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            AACEngine.FUNC_REGISTRY[func_alias] = func
            return func
        return decorator

    def __init__(self):
        self.sentence_bar: list[str] = []
        self.history: list[str] = []
        self.current_node: str = "HOME"
        self.tree: LanguageTree = load_language_tree()

    def _reset_history(self) -> None:
        self.current_node = "HOME"
        self.history.clear()

    def current_buttons(self) -> list[Button]:
        """Get the current buttons for the engine's current node,
        accounting for the universal node.
        If a node cannot be found in the language tree, it skips attempting
        to find buttons for the current node."""

        universal_node = self.tree.get("UNIVERSAL")
        node = self.tree.get(self.current_node)

        buttons: list[Button] = []

        if universal_node is not None:
            buttons.extend(universal_node.buttons)
        if node is not None:
            buttons.extend(node.buttons)
        else:
            if self.current_node not in _warned_nodes:
                print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: unspecified node: {COL_WARN}'{self.current_node}'{COL_END}", file=sys.stderr)
                _warned_nodes.add(self.current_node)

        return buttons

    def _on_lmb_button_press(self, button: Button) -> None:
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

        # If no word or dest, the button must have a function call inside of it
        if button.func is not None:
            func = AACEngine.FUNC_REGISTRY.get(button.func)
            if func is not None:
                func(self)
                return

            if button.func not in _warned_funcs:
                print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: unrecognised function: {COL_WARN}'{button.func}'{COL_END}", file=sys.stderr)
                _warned_funcs.add(button.func)

    def _handle_lmb_click(self, event: pg.event.Event) -> None:
        button_coord = _button_coord(event.pos)

        if button_coord is not None:
            if (button := _get_button_at_pos(self.current_buttons(), button_coord)):
                self._on_lmb_button_press(button)

    def _handle_rmb_click(self, event: pg.event.Event) -> None:
        # Right-click on a button or empty spot to add a button or
        # change its properties. This is 100% intended to be a user-facing feature.
        # People should be able to configure the AAC layout exactly to their needs.
        # Those proprietary suckers make you pay a representative to do it for you.

        # TODO: for now, this will only open a terminal interface
        # but eventually I'd like this make this a GUI and add drag-and-drop functionality

        button_coord = _button_coord(event.pos)

        # If the click does not correspond to a valid coordinate, return
        if not button_coord:
            return

        # Fetch the button at the coordinate
        button = _get_button_at_pos(self.current_buttons(), button_coord)

        # If the coordinate does not correspond to a valid on-screen
        # button, open the interface to create it, then early return
        if not button:
            # Prompt user for button properties
            label = input("enter a label for the new button: ").strip()
            if not label:
                print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: button label cannot be empty", file=sys.stderr)
                return

            word = input("enter a word for the button (or press Enter for none): ").strip() or None
            dest = input("enter a destination node for the button (or press Enter for none): ").strip() or None
            func = input(f"enter a function for the button (available: {', '.join(self.FUNC_REGISTRY.keys())}, or press Enter for none): ").strip() or None

            if not word and not dest and not func:
                print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: at least one of word, destination or func must be provided", file=sys.stderr)
                return

            # Validate function if provided
            if func and func not in self.FUNC_REGISTRY:
                print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: unrecognised function: {COL_WARN}'{func}'{COL_END}", file=sys.stderr)
                return

            button_type = input(f"enter a button type (or press Enter for 'default'): ").strip() or "default"

            # Provide a path to the image
            path_input = input(f"Enter a path to the image for the button (or press Enter to skip): ").strip() or None
            if path_input:
                path = Path(path_input).resolve()
                if not path.exists():
                    print(f"{COL_ERR}{COL_BOLD}error{COL_END}: no such image file: '{path}'", file=sys.stderr)
                    return
                if not path.is_file():
                    print(f"{COL_ERR}{COL_BOLD}error{COL_END}: not an image file: '{path}'", file=sys.stderr)
                    return

            # Create the new button
            new_button = Button(
                word=word,
                dest=dest,
                func=func,
                label=label,
                img=path_input,  # placeholder image path
                coords=button_coord,
                type=button_type
            )

            # Add button to current node and save
            # If the node doesn't exist, initialise a new node for the new button
            node = self.tree.get(self.current_node) or self.tree.add_node(self.current_node)
            node.buttons.append(new_button)
            save_language_tree(self.tree)
            return

        # Open the interface. Get an action: either 'modify', 'move', 'delete' or 'inspect'.
        # Once done, save the JSON to the nodes.json file.
        action = input("enter an action [modify | move | delete | inspect]: ").strip().lower()

        if action == "modify":
            if button.immutable:
                print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: refusing to modify immutable button", file=sys.stderr)
                return

            # Open the interface to modify the button's properties
            new_label = input(f"enter a new label for the button (old='{button.label}') or Enter to skip: ").strip()
            if new_label:
                button.label = new_label

            new_word, new_dest, new_func = None, None, None

            while (new_word is None and new_dest is None and new_func is None):
                new_word = input(f"enter a new word for the button (old='{button.word}') or Enter to skip: ").strip()
                if new_word:
                    button.word = new_word
                    break

                new_dest = input(f"enter a new destination node for the button (old='{button.dest}') or Enter to skip: ").strip()
                if new_dest:
                    button.dest = new_dest

                    # print a warning but do not block a user out of creating the new uninitialised node
                    if new_dest not in self.tree.nodes.keys():
                        print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: destination node does not exist in the language tree: {COL_WARN}'{new_dest}'{COL_END}. please click on the button to start initialising buttons in the new destination.", file=sys.stderr)

                new_func = input(f"enter a new function for the button (old='{button.func}', available: {', '.join(self.FUNC_REGISTRY.keys())}) or Enter to skip: ").strip()
                if new_func:
                    if new_func in self.FUNC_REGISTRY:
                        button.func = new_func
                        break
                    else:
                        print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: unrecognised function: {COL_WARN}'{new_func}'{COL_END}", file=sys.stderr)
                        new_func = None  # reset to loop again

                print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: at least one of word, dest or func must be provided", file=sys.stderr)

        elif action == "move":
            # If no button exists at the target coordinate, move the button to said target coordinate
            # If a button already exists there, swap positions between the button to move and the button already there
            # If the target coordinate is out of bounds, print an error message

            new_x = _read_positive_int_coord(GRID_W - 1, prompt=f"enter an integer coordinate value for the x-axis (0 to {GRID_W - 1}, old={button.coords[0]}): ")
            new_y = _read_positive_int_coord(GRID_H - 1, prompt=f"enter an integer coordinate value for the y-axis (0 to {GRID_H - 1}, old={button.coords[1]}): ")
            new_coords = (new_x, new_y)

            other_button: Button | None = _get_button_at_pos(self.current_buttons(), new_coords)

            if other_button is None:
                button.coords = new_coords
                return

            print("button already at target location - swapping positions")
            button.coords, other_button.coords = other_button.coords, button.coords

        elif action == "delete":
            # Fetch what node the button is in and delete the button from said node
            # We only need to check the UNIVERSAL node and the AACEngine's current node
            if button.immutable:
                print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: refusing to delete immutable button", file=sys.stderr)
                return

            for node_name in ["UNIVERSAL", self.current_node]:
                node = self.tree.get(node_name)
                if node and button in node.buttons:
                    node.buttons.remove(button)
                    save_language_tree(self.tree)
                    break
        elif action == 'inspect':
            # Inspect the button's properties
            for node_name in ["UNIVERSAL", self.current_node]:
                node = self.tree.get(node_name)
                if node and button in node.buttons:
                    print(button.inspect(node_label=node_name))
                    break
        else:
            print(f"{COL_WARN}{COL_BOLD}warning{COL_END}: unrecognised action: {COL_WARN}'{action}'{COL_END}", file=sys.stderr)

    def take_input(self, keys: ScancodeWrapper, events: list[pg.event.Event], dt_s: float) -> None:
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_lmb_click(event)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                self._handle_rmb_click(event)


# Now for registry functions
@AACEngine.register("clear_sentence_bar")
def clear_sentence_bar(self) -> None:
    """Clear the sentence bar."""
    self.sentence_bar.clear()

@AACEngine.register("backspace_sentence_bar")
def backspace_sentence_bar(self) -> None:
    """Remove the last word from the sentence bar."""
    if self.sentence_bar:
        self.sentence_bar.pop()

@AACEngine.register("speak_sentence_bar")
def speak_sentence_bar(self) -> None:
    """Speak the current sentence bar."""
    sentence = " ".join(self.sentence_bar)
    speak(sentence)

@AACEngine.register("stop_speaking")
def stop_speaking(self) -> None:
    """Stop any currently playing speech immediately."""
    _stop_speaking()
