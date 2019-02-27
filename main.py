import utime

from game import Game


def play():
    WIDHT = 3
    HEIGHT = WIDHT
    g = Game(WIDHT, HEIGHT)
    while True:
        try:
            g.step()
        except Exception:
            print("Oops...")
            g = Game(WIDHT, HEIGHT)
        # utime.sleep(1)


play()
