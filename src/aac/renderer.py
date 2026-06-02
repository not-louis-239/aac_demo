import pygame as pg

from .load_nodes import Button
from .engine import AACEngine
from .constants import (
    WN_W, WN_H,
    BUTTON_BORDER_WIDTH,
    BUTTON_FONT_SIZE,
    BUTTON_PADDING,
    BUTTON_TEXT_COLOR
)

class Renderer:
    def __init__(self, engine: AACEngine):
        self.engine = engine

    def _draw_button(self, button: Button) -> None:
        ...

    def draw(self, screen: pg.Surface) -> None:
        pass
