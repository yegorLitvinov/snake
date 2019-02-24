from game import Snake, Position, Direction


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
    

test_snake_calc_next_head_postion()
test_snake_move()