import math
import urandom
import utime


urandom.seed(utime.ticks_ms())


def randchoice(iterable) -> int:
    """Get random item from iterable."""
    length = len(iterable)
    index = urandom.getrandbits(int(math.log2(length)) + 2) % length
    return iterable[index]
