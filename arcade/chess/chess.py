""" Chess Program """

import arcade

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SQUARE = SCREEN_HEIGHT / 8


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Chess Example")
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def on_draw(self):
        self.clear()
        self.draw_grid()

    def draw_grid(self):
        y=SQUARE / 2
        for row in range(8):
            x=SQUARE / 2
            if row % 2 == 1:
                x = x + SQUARE
            for column in range(4):
                # X, Y, Width, Height
                arcade.draw_rect_filled(arcade.rect.XYWH(x , y, SQUARE , SQUARE ),arcade.color.WHITE)
                x=x+SQUARE*2
            y = y + SQUARE

def main():
    window = MyGame()
    arcade.run()


if __name__ == "__main__":
    main()