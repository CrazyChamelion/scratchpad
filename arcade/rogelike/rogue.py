import arcade
import math
from enum import Enum
import time 
import random
# Constants
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1300
SCREEN_TITLE = "RogueLike"
SHEET_PATH = "assets/urizen_onebit_tileset__v2d0.png"
DISPLAY_SCALE = 6
RAW_TILE_SIZE = 12
TILE_SIZE = RAW_TILE_SIZE * DISPLAY_SCALE

SPRITES_COORDS: dict[str, tuple[int, int, int, int]] = {
    "stone1": (1, 27, 12, 12),
    "stone2": (14, 27, 12, 12),
    "stonecorner1": (66, 27, 12, 12),
    "stonecorner2": (79, 27, 12, 12),
    "stonecorner3": (92, 27, 12, 12),
    "floor1": (1, 92, 12, 12),
    "floor2": (14, 92, 12, 12),
    "floor3": (27, 92, 12, 12),
    "player": (1015, 144, 12, 12)
}

EXAMPLE_LEVEL =[
    [2,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,1,1,1,1,1,1,1,1,2,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,2,2,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,2,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,2,0,2,2,2,2,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,2,2,2,2,2,2,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [2,1,1,1,1,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,1],
]

WORLD_HEIGH = len(EXAMPLE_LEVEL)
WORLD_WIDTH = len(EXAMPLE_LEVEL[0])

def tex_to_sprite(tex):
    return arcade.Sprite(tex, DISPLAY_SCALE)

class Rogue(arcade.Window):
    """
    Main application class.
    """
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.sheet = arcade.load_spritesheet(SHEET_PATH)
        self.map_sprites = arcade.SpriteList()
        self.player_sprites = arcade.SpriteList()
        self.player_x = random.randint(1,WORLD_WIDTH-2)
        self.player_y = random.randint(1,WORLD_HEIGH-2)
        self.player_tex = self.get_texture("player")
        self.setup_level()

    def setup_level(self):
        self.level_int = EXAMPLE_LEVEL
        self.wall_tex = self.get_texture("stone1")
        self.other_wall_tex = self.get_texture("stonecorner1")

    def get_texture(self, name: str) -> arcade.Sprite:
        x, y, w, h = SPRITES_COORDS[name]
        return self.sheet.get_texture(arcade.LBWH(x, y, w, h)) 

    def draw_player_centric(self):
        # draw the player
        self.player_sprites.clear()
        self.player_sprite = tex_to_sprite(self.player_tex)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        self.player_sprites.append(self.player_sprite)


        self.map_sprites.clear()
        for map_y in range(WORLD_HEIGH):
            for map_x in range(WORLD_WIDTH):
                if self.level_int[map_y][map_x] != 0:
                    if self.level_int[map_y][map_x] == 1:
                        sprite = tex_to_sprite(self.wall_tex)
                    elif self.level_int[map_y][map_x] == 2:
                        sprite = tex_to_sprite(self.other_wall_tex) 
                    sprite.center_x = (map_x - self.player_x) * TILE_SIZE + SCREEN_WIDTH // 2
                    sprite.center_y = (map_y - self.player_y) * TILE_SIZE + SCREEN_HEIGHT // 2
                    self.map_sprites.append(sprite)

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        #self.draw_world_centic()
        self.draw_player_centric()
        self.map_sprites.draw()
        self.player_sprites.draw()
        

    def on_update(self, delta_time):
        """ Movement and game logic """
        pass


    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed."""
        new_x = self.player_x
        new_y = self.player_y
        if symbol == arcade.key.W:
           new_y += 1 
        elif symbol == arcade.key.S:
           new_y -= 1 
        elif symbol == arcade.key.A:
           new_x -= 1 
        elif symbol == arcade.key.D:
           new_x += 1 
        # inside the map
        if new_x < WORLD_WIDTH and new_y < WORLD_WIDTH and new_x >= 0 and new_y >= 0:
            # not setpping into a wall
            if self.level_int[new_y][new_x] == 0:
                self.player_x = new_x
                self.player_y = new_y

def main():
    """ Main method"""
    game = Rogue()
    arcade.run()

if __name__ == "__main__":
    main()