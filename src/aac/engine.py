import pygame as pg
from pygame.key import ScancodeWrapper

from .load_nodes import Button, LanguageTree, load_language_tree

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
                self.current_node = button.dest

        # Clear history if at HOME or history is exhausted
        if self.current_node == "HOME" or not self.history:
            self._reset_history()

        # Append word to sentence bar if the button has one
        if button.word is not None:
            self.sentence_bar.append(button.word)

    def take_input(self, keys: ScancodeWrapper, events: list[pg.event.Event], dt_s: float) -> None:
        ...  # TODO: implement input handling logic
