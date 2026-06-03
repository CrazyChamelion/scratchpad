import arcade
import math
from enum import Enum
import time 
import random
from level_gen import generate_level 

# Constants
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1300
SCREEN_TITLE = "RogueLike"
SHEET_PATH = "assets/urizen_onebit_tileset__v2d0.png"
DISPLAY_SCALE = 3
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
    "player": (1015, 144, 12, 12),
    "exit": (196, 14, 12, 12)
}

class enemy():
    def __init__(self, health, damage, ai,sprite,x,y):
        self.health = health 
        self.damage = damage
        self.ai = ai
        self.sprite = sprite 
        self.x = x
        self.y = y
    def pos(self):
        return (self.x) , (self.y)
    def stats(self):
        return (self.health) , (self.damage)
    def ai(self):
        return str(self.ai)
    def sprite(self):
        return str(self.sprite)
enemies = [enemy(1,2,"ranged","goblin",1,2), enemy(2,1,"mele","skeleton",1,1), enemy(1,3,"flanker","ork",2,1)]
for a in enemies:
    print (a.pos() , a.stats(), a.ai(), a.sprite() )


WORLD_HEIGH = 100
WORLD_WIDTH = 100

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
        self.exit_x = random.randint(1,WORLD_WIDTH-2)
        self.exit_y = random.randint(1,WORLD_HEIGH-2)
        self.player_tex = self.get_texture("player")
        self.gamewin = False
        self.setup_level()
        while self.level_int [self.player_y] [self.player_x] != 0:
            self.player_x = random.randint(1,WORLD_WIDTH-2)
            self.player_y = random.randint(1,WORLD_HEIGH-2)
        while self.level_int [self.exit_y] [self.exit_x] != 0:
            self.exit_x = random.randint(1,WORLD_WIDTH-2)
            self.exit_y = random.randint(1,WORLD_HEIGH-2)


    def setup_level(self):
        self.level_int = generate_level(WORLD_WIDTH,WORLD_HEIGH, target_area=500)
        self.wall_tex = self.get_texture("stone1")
        self.other_wall_tex = self.get_texture("stonecorner1")
        self.exit_tex = self.get_texture("exit")
        
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
        #draw exit
        exit_sprite = tex_to_sprite(self.exit_tex)
        exit_sprite.center_x = (self.exit_x - self.player_x) * TILE_SIZE + SCREEN_WIDTH // 2
        exit_sprite.center_y = (self.exit_y - self.player_y) * TILE_SIZE + SCREEN_HEIGHT // 2
        self.map_sprites.append(exit_sprite)
        #draw map
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
        if self.player_x == self.exit_x and self.player_y == self.exit_y:
            self.gamewin = True
        if self.gamewin:
            print("win")



    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed."""
        newx = self.player_x
        newy = self.player_y
        if symbol == arcade.key.A:
            newx = self.player_x-1
        elif symbol == arcade.key.D:
            newx = self.player_x+1
        elif symbol == arcade.key.S:
            newy = self.player_y-1
        elif symbol == arcade.key.W:
            newy = self.player_y+1
        if self.level_int [newy] [newx] == 0:
            self.player_x = newx
            self.player_y = newy  

def main():
    """ Main method"""
    game = Rogue()
    arcade.run()

if __name__ == "__main__":
    main()