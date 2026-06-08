from enum import Enum

import arcade

# Constants for window size and title
SCREEN_WIDTH = 3100
SCREEN_HEIGHT = 2100
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
            self.p.x * scale + SCREEN_CENTER_X,
            self.p.y * scale + SCREEN_CENTER_Y,
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
        arcade.set_background_color(arcade.color.WHITE)
        self.rows = 70
        self.cols = 70
        self.zoom = 20
        self.turns_per_frame = 10
        self.go_on_update = False
        self.squares = []
        self.generate_grid_lines()
        for j in range(self.rows):
            y = j - self.rows // 2
            row = []
            for i in range(self.cols):
                x = i - self.cols // 2
                row.append(Square(Vector(x, y), Color.WHITE))
            self.squares.append(row)

        # shape list seemst to have a maximum size on my system and screws up when I go past it
        # self.black_squares = arcade.shape_list.ShapeElementList()
        self.black_squares = arcade.SpriteList()
        self.ant = Ant(Vector(0.5, 0.5), Direction.UP)
        self.running = True
        self.turn_count = 0

    def generate_black_squares(self):
        # self.black_squares = arcade.shape_list.ShapeElementList()
        self.black_squares.clear()
        for j in range(self.rows):
            y = (j - self.rows / 2) * self.zoom + SCREEN_CENTER_Y + self.zoom / 2
            for i in range(self.cols):
                if self.squares[j][i].color == Color.BLACK:
                    x = (
                        (i - self.cols / 2) * self.zoom
                        + SCREEN_CENTER_X
                        + self.zoom / 2
                    )
                    # using ShapeElementList and geometry has a bug
                    # square = arcade.shape_list.create_rectangle_filled(
                    #    center_x=x,
                    #    center_y=y,
                    #    width=self.zoom,
                    #    height=self.zoom,
                    #    color=arcade.color.BLACK,
                    # )
                    square = arcade.SpriteSolidColor(
                        self.zoom, self.zoom, x, y, arcade.color.BLACK
                    )
                    self.black_squares.append(square)

    def generate_grid_lines(self):
        # vertical lines
        self.vertical_grid_lines = arcade.shape_list.ShapeElementList()
        bottom_y = 0
        top_y = SCREEN_HEIGHT
        points = []
        for i in range(self.cols + 1):
            x = (i - self.cols / 2) * self.zoom + SCREEN_CENTER_X
            points.append((x, bottom_y))
            points.append((x, top_y))
        self.vertical_grid_lines.append(
            arcade.shape_list.create_lines(points, arcade.color.BLUE)
        )

        # horizontal Lines
        points.clear()
        left_x = 0
        right_x = SCREEN_WIDTH
        self.horizontal_grid_lines = arcade.shape_list.ShapeElementList()
        for j in range(self.rows + 1):
            y = (j - self.rows / 2) * self.zoom + SCREEN_CENTER_Y
            points.append((left_x, y))
            points.append((right_x, y))
        self.horizontal_grid_lines.append(
            arcade.shape_list.create_lines(points, arcade.color.BLUE)
        )

    def on_draw(self):
        """Renders the screen (called 60 times/sec)."""
        self.clear()
        # for j in range(self.rows):
        #    for i in range(self.cols):
        #        self.squares[j][i].draw(self.zoom)
        self.vertical_grid_lines.draw()
        self.horizontal_grid_lines.draw()
        self.black_squares.draw()
        self.ant.draw(self.zoom)
        arcade.draw_text(
            f"Turns: {self.turn_count}",
            SCREEN_WIDTH - 20,
            SCREEN_HEIGHT - 20,
            arcade.color.BLACK,
            font_size=24,
            anchor_x="right",
            anchor_y="top",
        )

    def on_update(self, delta_time):
        """Handles game logic and movement."""
        if self.go_on_update:
            if self.running:
                # 10 turns per frame
                for i in range(self.turns_per_frame):
                    if self.running:
                        self.take_turn()
                self.generate_black_squares()

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
            self.turn_count += 1

    def on_key_press(self, key, modifiers):
        """Handles user input."""
        if key == arcade.key.ENTER:
            self.go_on_update = not self.go_on_update
        if key == arcade.key.SPACE:
            self.take_turn()
            self.generate_black_squares()
        if key == arcade.key.ESCAPE:
            self.close()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.zoom += scroll_y
        if self.zoom < 3:
            self.zoom = 3
        self.generate_grid_lines()
        self.generate_black_squares()


def main():
    window = Game()
    arcade.run()


if __name__ == "__main__":
    main()
