from enum import Enum

import arcade

# Constants for window size and title
SCREEN_WIDTH = 3100
SCREEN_HEIGHT = 2400
SCREEN_CENTER_X = SCREEN_WIDTH // 2
SCREEN_CENTER_Y = SCREEN_HEIGHT // 2
SCREEN_TITLE = "Arcade Starter Template"


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Color(Enum):
    WHITE = 1
    BLACK = 2


class Square:
    def __init__(self, ll, color):
        self.ll = ll
        self.color = color

    def flip(self):
        if self.color == Color.BLACK:
            self.color = Color.WHITE
        else:
            self.color = Color.BLACK

    def point_is_in(self, p):
        # in x
        if self.ll.x < p.x and p.x < self.ll.x + 1:
            # in y
            if self.ll.y < p.y and p.y < self.ll.y + 1:
                return True
        return False

    def draw(self, scale):
        color = arcade.color.BLACK
        if self.color == Color.WHITE:
            color = arcade.color.WHITE
        ll = Vector(
            self.ll.x * scale + SCREEN_CENTER_X, self.ll.y * scale + SCREEN_CENTER_Y
        )
        arcade.draw_rect_filled(
            arcade.rect.XYWH(ll.x + 1, ll.y + 1, scale - 2, scale - 2), color
        )


class Direction(Enum):
    RIGHT = 1
    UP = 2
    LEFT = 3
    DOWN = 4


class Ant:
    def __init__(self, p, dir):
        self.p = p
        self.dir = dir

    def draw(self, scale):
        r = scale / 2
        p = Vector(
            self.p.x * scale + SCREEN_CENTER_X - r,
            self.p.y * scale + SCREEN_CENTER_Y - r,
        )
        arcade.draw_circle_filled(p.x, p.y, r, arcade.color.RED)
        end = Vector(p.x, p.y)
        if self.dir == Direction.RIGHT:
            end.x += r
        if self.dir == Direction.UP:
            end.y += r
        if self.dir == Direction.LEFT:
            end.x -= r
        if self.dir == Direction.DOWN:
            end.y -= r
        arcade.draw_line(p.x, p.y, end.x, end.y, arcade.color.WHITE)

    def turn_right(self):
        if self.dir == Direction.RIGHT:
            self.dir = Direction.DOWN
        elif self.dir == Direction.UP:
            self.dir = Direction.RIGHT
        elif self.dir == Direction.LEFT:
            self.dir = Direction.UP
        elif self.dir == Direction.DOWN:
            self.dir = Direction.LEFT

    def turn_left(self):
        if self.dir == Direction.RIGHT:
            self.dir = Direction.UP
        elif self.dir == Direction.UP:
            self.dir = Direction.LEFT
        elif self.dir == Direction.LEFT:
            self.dir = Direction.DOWN
        elif self.dir == Direction.DOWN:
            self.dir = Direction.RIGHT

    def move(self):
        if self.dir == Direction.RIGHT:
            self.p.x += 1
        elif self.dir == Direction.UP:
            self.p.y += 1
        elif self.dir == Direction.LEFT:
            self.p.x -= 1
        elif self.dir == Direction.DOWN:
            self.p.y -= 1


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLUE)
        self.rows = 46
        self.cols = 62
        self.zoom = 20
        self.squares = []

        for j in range(self.rows):
            y = j - self.rows // 2
            row = []
            for i in range(self.cols):
                x = i - self.cols // 2
                row.append(Square(Vector(x, y), Color.WHITE))
            self.squares.append(row)
        self.ant = Ant(Vector(0.5, 0.5), Direction.UP)
        self.running = True

    def on_draw(self):
        """Renders the screen (called 60 times/sec)."""
        self.clear()
        for j in range(self.rows):
            for i in range(self.cols):
                self.squares[j][i].draw(self.zoom)
        self.ant.draw(self.zoom)

    def on_update(self, delta_time):
        """Handles game logic and movement."""
        if self.running:
            # 10 turns per frame
            for i in range(100):
                if self.running:
                    self.take_turn()

    def get_square_with_ant(self):
        x = int(self.ant.p.x - 0.5)
        i = int(x + self.cols / 2)
        y = int(self.ant.p.y - 0.5)
        j = int(y + self.rows / 2)
        if (i < 0 or i >= self.cols) or (j < 0 or j >= self.rows):
            self.running = False
            return None
        return self.squares[j][i]

    def take_turn(self):
        # if ant is on white square:
        #   turn right, change square black, move forward
        # else:
        #   turn left, change square white, move forward

        # find what square we are on
        s = self.get_square_with_ant()
        if s:
            if s.color == Color.WHITE:
                self.ant.turn_right()
            else:
                self.ant.turn_left()
            s.flip()
            self.ant.move()

    def on_key_press(self, key, modifiers):
        """Handles user input."""
        if key == arcade.key.SPACE:
            self.take_turn()
        if key == arcade.key.ESCAPE:
            self.close()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.zoom += scroll_y
        if self.zoom < 3:
            self.zoom = 3


def main():
    window = Game()
    arcade.run()


if __name__ == "__main__":
    main()
