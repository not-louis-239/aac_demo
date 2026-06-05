# constants.py - program constants
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


from dataclasses import dataclass
from typing import TypeAlias

Colour: TypeAlias = tuple[int, int, int]

@dataclass(frozen=True, kw_only=True)
class Theme:
    display_name: str
    bg_colour: Colour
    fg_colour: Colour
    fitzgerald_theme: dict[str, Colour]

FPS = 60

WN_W, WN_H = 1280, 720
SENTENCE_BAR_H = 80

# How many buttons to have in the button area
GRID_W, GRID_H = 10, 6

BUTTON_BORDER_WIDTH = 2

# Relative to WN_W, WN_H
UI_PADDING = WN_W * 0.01
BUTTON_FONT_SIZE = WN_W * 0.015

IMAGE_SIZE = int((WN_H - SENTENCE_BAR_H - UI_PADDING) / GRID_H * 0.65)

THEMES: list[Theme] = [
    # Light mode
    Theme(
        display_name="Light",
        bg_colour=(255, 255, 255),
        fg_colour=(0, 0, 0),
        fitzgerald_theme={
            "pronoun": (255, 255, 180),
            "noun": (255, 210, 180),
            "verb": (180, 255, 180),
            "descriptor": (180, 200, 255),
            "social": (240, 180, 255),
            "syntax": (180, 180, 180),
            "system": (240, 240, 240)
        }
    ),

    # Dark mode
    Theme(
        display_name="Dark",
        bg_colour=(50, 50, 50),
        fg_colour=(255, 255, 255),
        fitzgerald_theme={
            "pronoun": (100, 100, 50),
            "noun": (100, 75, 50),
            "verb": (50, 100, 50),
            "descriptor": (50, 65, 100),
            "social": (90, 50, 100),
            "syntax": (70, 70, 70),
            "system": (55, 55, 55)
        }
    )
]

def _test():
    BOLD = "\033[1m"
    RESET = "\033[0m"
    GREY_BG = "\033[48;2;120;120;120m"

    for theme in THEMES:
        name = theme.display_name

        print(f"\nTheme: {name}")
        print("Colors:")

        col = theme.bg_colour
        r, g, b = col
        col_code = f"\033[38;2;{r};{g};{b}m"
        text = f"  bg_colour: {BOLD}{GREY_BG}{col_code}{col}{RESET}"
        print(text)

        col = theme.fg_colour
        r, g, b = col
        col_code = f"\033[38;2;{r};{g};{b}m"
        text = f"  fg_colour: {BOLD}{GREY_BG}{col_code}{col}{RESET}"
        print(text)

        for cat, col in theme.fitzgerald_theme.items():
            r, g, b = col
            col_code = f"\033[38;2;{r};{g};{b}m"
            text = f"  {cat}: {BOLD}{GREY_BG}{col_code}{col}{RESET}"
            print(text)

if __name__ == "__main__":
    _test()
