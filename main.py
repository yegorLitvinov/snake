import utime

from game import Game


WIDHT = 10
HEIGHT = 10
g = Game(WIDHT, HEIGHT)


while True:
    g.step()
    # utime.sleep(1)