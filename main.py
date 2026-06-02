#!/usr/bin/env python3

import sys
from pathlib import Path

import pygame as pg

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from aac.constants import WN_W, WN_H, FPS
from aac.aac_main import AAC

def main():
    pg.init()

    screen = pg.display.set_mode((WN_W, WN_H))
    pg.display.set_caption("AAC")
    clock = pg.time.Clock()
    aac = AAC()

    running = True
    while running:
        keys = pg.key.get_pressed()
        events = pg.event.get()
        dt_s = clock.tick(FPS) / 1_000.0

        for event in events:
            if event.type == pg.QUIT:
                running = False

        aac.update(dt_s=dt_s)
        aac.take_input(keys=keys, events=events, dt_s=dt_s)
        aac.draw(screen)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExited.")
        pg.quit()
