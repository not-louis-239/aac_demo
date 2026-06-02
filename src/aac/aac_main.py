import pygame as pg
from pygame.key import ScancodeWrapper

from aac.engine import AACEngine
from aac.renderer import Renderer

class AAC:
    def __init__(self):
        self.engine = AACEngine()
        self.renderer = Renderer(engine=self.engine)

    def update(self, dt_s: float) -> None:
        pass

    def take_input(self, keys: ScancodeWrapper, events: list[pg.event.Event], dt_s: float) -> None:
        self.engine.take_input(keys=keys, events=events, dt_s=dt_s)

    def draw(self, screen: pg.Surface) -> None:
        self.renderer.draw(screen=screen)
