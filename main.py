import utime

from game import Game


WIDHT = 4
HEIGHT = 4
g = Game(WIDHT, HEIGHT)


while True:
    g.step()
    # utime.sleep(1)