from game import Snake, Position, Direction, Apple
from utils import randchoice


def test_position():
    p1 = Position(1, 2)
    p2 = p1.copy()
    assert p1 == p2
    p1.x = 4
    assert p2.x == 1
    assert p2.y == 2
    assert p1 != p2


def test_snake_calc_next_head_postion():
    snake = Snake(3, 3, Position(1, 1), Direction.RIGHT)

    position = snake._calc_next_head_position(Direction.RIGHT)
    assert position.x == 2
    assert position.y == 1

    position = snake._calc_next_head_position(Direction.LEFT)
    assert position.x == 0
    assert position.y == 1

    position = snake._calc_next_head_position(Direction.UP)
    assert position.x == 1
    assert position.y == 0

    position = snake._calc_next_head_position(Direction.DOWN)
    assert position.x == 1
    assert position.y == 2


def test_snake_move():
    snake = Snake(3, 3, Position(1, 1), Direction.RIGHT)
    snake.move(None)
    assert snake.head.current_position.x == 2
    assert snake.head.current_position.y == 1
    assert snake.direction == Direction.RIGHT

    snake.move(Direction.UP)
    assert snake.head.current_position.x == 2
    assert snake.head.current_position.y == 0
    assert snake.direction == Direction.UP
    

def test_apple_respawn():
    size = 3
    matrix = [
        ["#", "", ""],
        ["#", "#", ""],
        ["#", "", "#"],
    ]
    apple = Apple(size, size)
    assert apple.position.x == 0
    assert apple.position.y == 0
    for i in range(100):
        apple.respawn(matrix)
        x = apple.position.x
        y = apple.position.y
        assert 0 <= x < size
        assert 0 <= y < size
        assert x != y
        assert x != 0


def test_randchoice():
    size = 10
    iterable = [i for i in range(size)]
    counter = {i: 0 for i in range(size)}
    for i in range(10000):
        choice = randchoice(iterable)
        counter[choice] += 1
    print("'randchoice' results:")
    for key, value in counter.items():
        print("{}:\t{:.1f}%".format(key, value / 100))


test_position()
test_snake_calc_next_head_postion()
test_snake_move()
test_apple_respawn()
test_randchoice()