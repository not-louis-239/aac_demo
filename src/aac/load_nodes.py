from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json

from aac.paths import NODES_FILE

_TYPE_DISPLAY_COL = "\033[93m"
_WORD_DISPLAY_COL = "\033[32m"
_DEST_DISPLAY_COL = "\033[94m"
_END = "\033[0m"

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

@dataclass
class Node:
    buttons: list[Button]

@dataclass
class LanguageTree:
    nodes: dict[str, Node] = field(default_factory=dict)

    def __getitem__(self, k: str) -> Node:
        return self.nodes[k]

def load_language_tree() -> LanguageTree:
    with open(NODES_FILE) as f:
        data_raw = json.load(f)

    nodes_raw: dict[str, Any] = data_raw["nodes"]
    nodes: dict[str, Node] = {}

    for node_name, node_dict in nodes_raw.items():
        buttons_raw_list = node_dict["buttons"]

        node_buttons: list[Button] = []
        for button_raw in buttons_raw_list:
            button = Button(
                label=button_raw["label"],
                dest=button_raw.get("dest", None),
                coords=tuple(button_raw["coords"]),
                type=button_raw["type"],
                word=button_raw.get("word", None),
                img=button_raw.get("img", None),
            )
            node_buttons.append(button)

        node = Node(buttons=node_buttons)
        nodes[node_name] = node

    return LanguageTree(nodes=nodes)

def print_lt(lt: LanguageTree) -> None:
    for node_name, node in lt.nodes.items():
        print(f"[{node_name}]")

        for button in node.buttons:
            line = (
                f"  - {button.label!r} {_TYPE_DISPLAY_COL}[{button.type}]{_END}"
                + (f"{_DEST_DISPLAY_COL} -> {button.dest!r}{_END}," if button.dest else ",")
                + (f"{_WORD_DISPLAY_COL} word: {button.word!r}{_END}," if button.word else "")
                + f" coords: {button.coords},"
                + f" img: '{button.img}'"
            )

            print(line)

        print()

def _test():
    lt = load_language_tree()
    print_lt(lt)

if __name__ == "__main__":
    _test()
