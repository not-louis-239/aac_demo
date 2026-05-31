from dataclasses import dataclass
from pathlib import Path

@dataclass
class Button:
    # How it acts
    word: str | None
    dest: str | int | None   # target folder OR relative offset

    # How it looks
    label: str
    img: Path                # relative path to image folder from assets/images
    coords: tuple[int, int]  # (x, y) from [-6..-1] U [0..5]
    type: str                # used for button highlighting

class AACEngine:
    """The engine class for the AAC talker (AAC = Augmentative and Alternative Communication)."""

    def __init__(self):
        self.sentence_bar: list[str] = []
        self.history: list[str] = []
        self.current_node: str = "HOME"

    def reset_history(self) -> None:
        self.current_node = "HOME"
        self.history.clear()

    def on_button_press(self, button: Button) -> None:
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
            self.reset_history()

        # Append word to sentence bar if the button has one
        if button.word is not None:
            self.sentence_bar.append(button.word)
