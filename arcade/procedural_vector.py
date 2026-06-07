import arcade
import math
import random
# Constants for window size and title
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Starter Template"


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# pull info out of the class example (procedural)
def add_vec(a, b):
    return Vector(a.x + b.x, a.y + b.y)

def subtract_vec(a, b):
    return Vector(a.x - b.x, a.y - b.y)

def scale_vec(v, scale):
    return Vector(v.x*scale, v.y*scale)

def length_vec(v):
    return math.sqrt(v.x*v.x + v.y*v.y)

def normalize_vec(v):
    l = length_vec(v)
    return scale_vec(v, 1 / l)

def random_vec():
    return Vector(random.randint(1,SCREEN_WIDTH),random.randint(1,SCREEN_HEIGHT))

class Arrow:
    def __init__(self, p, dir):
        self.p = p
        self.dir = dir

# procedural draw arrow
def draw_arrow(a):
    start = a.p
    arcade.draw_point(x=start.x, y=start.y, color=arcade.color.GREEN, size=5)
    end = add_vec(a.p, a.dir)
    arcade.draw_point(x=end.x, y=end.y, color=arcade.color.RED, size=5)

    arcade.draw_line(
        start_x=start.x,
        start_y=start.y,
        end_x=end.x,
        end_y=end.y,
        color=arcade.color.WHITE,
        line_width=3,
    )


class VectorDrawer(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.player = random_vec()
        self.enemies = []
        for a in range (10):
            e = random_vec()
            between = subtract_vec(e,self.player)
            while length_vec(between) < 100: 
                e = random_vec()
                between = subtract_vec(e,self.player)
            self.enemies.append (e)
                
                 
        self.arrows = []
        for e in self.enemies:
            dir = subtract_vec(self.player,e)
            p = length_vec(dir)
            dir = normalize_vec(dir) 
            dir = scale_vec(dir,50)
            self.arrows.append(Arrow(e,dir))



    def setup(self):
        """Initializes game variables and objects."""
        pass

    def on_draw(self):
        """Renders the screen (called 60 times/sec)."""
        self.clear()
        for a in self.arrows:
            draw_arrow(a)
        arcade.draw_circle_filled(self.player.x , self.player.y , 10 , arcade.color.BLUE)
        for i in self.enemies:
            arcade.draw_circle_filled(i.x , i.y , 10 , arcade.color.RED)
    def on_update(self, delta_time):
        """Handles game logic and movement."""
        pass

    def on_key_press(self, key, modifiers):
        """Handles user input."""
        if key == arcade.key.ESCAPE:
            self.close()


def main():
    window = VectorDrawer()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
