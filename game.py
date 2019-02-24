from utils import randchoice


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "x: {}, y: {}".format(self.x, self.y)
    
    def copy(self):
        return Position(self.x, self.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Vertebra:
    def __init__(self, current_position: Position, next_position: Position):
        self.current_position = current_position
        self.next_position = next_position

    def __str__(self):
        return "Current: {}, Next: {}".format(self.current_position, self.next_position)


class Direction:
    UP = -1
    DOWN = 1
    LEFT = -2
    RIGHT = 2


class DrawableObject:
    EMPTY = 1
    APPLE = 2
    SNAKE = 3
    

class Snake:
    def __init__(self, width, height, initial_position: Position, direction: int):
        self.width = width
        self.height = height
        self.direction = direction
        head = Vertebra(initial_position, None)
        self.skeleton = [head]
        self.is_eating = False
    
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
        next_position = self.head.current_position.copy()
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
        next_position = self._calc_next_head_position(direction)
        if self.is_eating:
            self.is_eating = False
            # Apple has been eaten, create new head
            self.head.next_position = next_position.copy()
            vertebra = Vertebra(next_position.copy(), None)
            self.skeleton.insert(0, vertebra)
        else:
            self.head.current_position = next_position
            for i in range(1, len(self.skeleton)):
                self.skeleton[i].current_position = self.skeleton[i].next_position
                self.skeleton[i].next_position = self.skeleton[i - 1].current_position
        if direction is not None:
            self.direction = direction

    def eat(self):
        self.is_eating = True


class Apple:
    def __init__(self, height: int, width: int):
        self.position = Position(0, 0)
        self.width = width
        self.height = height
    
    def respawn(self, matrix: list):
        non_full_row_indexes = [i for i in range(self.height) if not all(matrix[i])]
        y = randchoice(non_full_row_indexes)
        non_full_col_indexes = [j for j in range(self.width) if not matrix[y][j]]
        x = randchoice(non_full_col_indexes)
        self.position.x = x
        self.position.y = y


class BaseDisplay:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.matrix = [[False for j in range(width)] for i in range(height)]

    def set_position(self, position: Position, obj):
        self.matrix[position.y][position.x] = obj
    
    def clear(self):
        for i in range(self.height):
            for j in range(self.width):
                self.matrix[i][j] = False

    def draw(self):
        raise NotImplementedError()


class ConsoleDisplay(BaseDisplay):
    def draw(self):
        print("")
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j] == DrawableObject.SNAKE:
                    print("#", end="")
                elif self.matrix[i][j] == DrawableObject.APPLE:
                    print("@", end="")
                else:
                    print(".", end="")
            print("")
        print("")
    

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
        self.apple = Apple(width, height)
        self.display = ConsoleDisplay(width, height)
        self.apple.respawn(self.display.matrix)
        self.controller = Controller()
    
    def step(self):
        self.display.clear()
        direction = self.controller.get_direction()
        self.snake.move(direction)
        if self.snake.head.current_position == self.apple.position:
            self.snake.eat()
            self.apple.respawn(self.display.matrix)
        for vertebra in self.snake.skeleton:
            self.display.set_position(vertebra.current_position, DrawableObject.SNAKE)
        self.display.set_position(self.apple.position, DrawableObject.APPLE)
        self.display.draw()
