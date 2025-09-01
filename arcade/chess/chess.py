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
        self.reset_board()

    def reset_board(self):
        self.white_sprite_list = arcade.SpriteList()
        self.black_sprite_list = arcade.SpriteList()

        w_pawn = arcade.Sprite("./assets/white-pawn.png")
        w_pawn.width = SQUARE
        w_pawn.height = SQUARE
        w_pawn.center_x = SQUARE/2
        w_pawn.center_y = SQUARE+SQUARE/2
        self.white_sprite_list.append(w_pawn)

        b_pawn = arcade.Sprite("./assets/black-pawn.png")
        b_pawn.width = SQUARE
        b_pawn.height = SQUARE
        b_pawn.center_x = SQUARE/2
        b_pawn.center_y = (SQUARE * 8) - SQUARE - SQUARE/2
        self.black_sprite_list.append(b_pawn)

    def on_draw(self):
        self.clear()
        self.draw_grid()
        self.white_sprite_list.draw()
        self.black_sprite_list.draw()

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