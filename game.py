from ucollections import namedtuple


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __str__(self):
        print("x: {}, y: {}".format(self.x, self.y))


class Vertebra:
    def __init__(self, current_position: Position, next_position: Position):
        self.current_position = current_position
        self.next_position = next_position

    def __str__(self):
        print("Current: {}, Next: {}".format(self.current_position, self.next_position))


class Direction:
    UP = -1
    DOWN = 1
    LEFT = -2
    RIGHT = 2


class Snake:
    def __init__(self, width, height, initial_position: Position, direction: int):
        self.width = width
        self.height = height
        self.direction = direction
        head = Vertebra(initial_position, None)
        self.skeleton = [head]
    
    @property
    def head(self):
        return self.skeleton[0]

    def _calc_next_head_direction(self, direction):
        if direction is None:
            # No move to the same direction as previously
            direction = self.direction
        if direction == -self.direction:
            # Ban 180 degree rotation
            direction = self.direction
        return direction

    def _calc_next_head_position(self, direction: int) -> Position:
        next_position = Position(self.head.current_position.x, self.head.current_position.y)
        if direction == Direction.UP:
            next_position.y -= 1
        elif direction == Direction.DOWN:
            next_position.y += 1
        elif direction == Direction.LEFT:
            next_position.x -= 1
        elif direction == Direction.RIGHT:
            next_position.x += 1
            
        # Slam into wall
        if next_position.y >= self.height:
            next_position.y = 0
        elif next_position.y < 0:
            next_position.y = self.height - 1
        if next_position.x >= self.width:
            next_position.x = 0
        elif next_position.x < 0:
            next_position.x = self.width - 1

        return next_position

    def move(self, direction):
        direction = self._calc_next_head_direction(direction)
        self.head.current_position = self._calc_next_head_position(direction)
        if direction is not None:
            self.direction = direction
        for i in range(1, len(self.skeleton)):
            self.skeleton[i].next_position = self.skeleton[i - 1].current_position


class BaseDisplay:
    def __init__(self, width, height):
        raise NotImplementedError()

    def set_position(self, x: int, y: int):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()


class ConsoleDisplay(BaseDisplay):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.display = [[False for j in range(width)] for i in range(height)]

    def set_position(self, position: Position):
        print(position)
        self.display[position.y][position.x] = True
    
    def draw(self):
        print("")
        for i in range(self.height):
            for j in range(self.width):
                if (self.display[i][j]):
                    print("*", end="")
                else:
                    print(".", end="")
            print("")
        print("")
    
    def clear(self):
        for i in range(self.height):
            for j in range(self.width):
                self.display[i][j] = False


class Controller:
    def get_direction(self) -> int:
        print("Enter key: ")
        chars = input()
        if not chars:
            return None
        key = chars[-1]
        if key == "w":
            return Direction.UP
        if key == "s":
            return Direction.DOWN
        if key == "a":
            return Direction.LEFT
        if key == "d":
            return Direction.RIGHT
        return None


class Game:
    def __init__(self, width: int, height: int):
        initial_position = Position(int(width / 2), int(height / 2))
        self.snake = Snake(width, height, initial_position, Direction.RIGHT)
        self.display = ConsoleDisplay(width, height)
        self.controller = Controller()
    
    def step(self):
        self.display.clear()
        direction = self.controller.get_direction()
        print(direction)
        self.snake.move(direction)
        for vertebra in self.snake.skeleton:
            self.display.set_position(vertebra.current_position)
        
        self.display.draw()
        