# aac_main.py - module to store main AAC class
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

from aac.asset_manager import Assets
from aac.engine import AACEngine
from aac.renderer import Renderer

class AAC:
    def __init__(self):
        self.engine = AACEngine()
        self.renderer = Renderer(aac_inst=self)
        self.assets = Assets()

    def update(self, dt_s: float) -> None:
        pass

    def take_input(self, keys: ScancodeWrapper, events: list[pg.event.Event], dt_s: float) -> None:
        self.engine.take_input(keys=keys, events=events, dt_s=dt_s)

    def draw(self, screen: pg.Surface) -> None:
        self.renderer.draw(screen=screen)
