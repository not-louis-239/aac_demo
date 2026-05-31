WN_W, WN_H = 1280, 720
SENTENCE_BAR_H = 100

# How many buttons to have in the button area
GRID_W, GRID_H = 6, 6

BUTTON_BORDER_WIDTH = 2
BUTTON_TEXT_COLOR = (0, 0, 0)

# Relative to WN_W, WN_H
BUTTON_PADDING = WN_W * 0.01
BUTTON_FONT_SIZE = WN_W * 0.015

FITZGERALD_THEME: dict[str, tuple[int, int, int]] = {
    "pronoun": (255, 255, 180),
    "noun": (255, 210, 180),
    "verb": (180, 255, 180),
    "descriptor": (180, 200, 255),
    "social": (240, 180, 255),
    "syntax": (180, 180, 180),
    "system": (255, 255, 255)
}

def _test():
    for cat, colour in FITZGERALD_THEME.items():
        r, g, b = colour
        text = f"\033[38;2;{r};{g};{b}m\033[1m{cat}\033[0m"
        print(text)

if __name__ == "__main__":
    _test()
