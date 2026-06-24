import arcade
import math
from enum import Enum
import time 
import random
from level_gen import generate_level 
from astar import astar_flood

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
    "stonecorner1": (66, 27, 12, 12),
    "player": (1015, 183, 12, 12),
    "exit": (196, 14, 12, 12),
    "goblin": (1353, 53, 12, 12),
    "skeleton": (1353, 131, 12, 12),
    "troll": (1353, 118, 12, 12),
    "sword" : (508, 79, 12, 12),
}

class enemy():
    def __init__(self, health, damage, ai,texture,x,y):
        self.health = health 
        self.damage = damage
        self.ai = ai
        self.texture = texture
        self.x = x
        self.y = y
        self.speed = 2

    def doai(self,astarmap):
        currentpos = astarmap [self.y][self.x]
        north = None
        south = None
        east = None
        west = None
        if self.y+self.speed < len(astarmap):
            north =  astarmap [self.y+self.speed][self.x]
        if self.y-self.speed > 0:
            south = astarmap [self.y-self.speed][self.x]
        if self.x+self.speed < len(astarmap[0]):
            east = astarmap [self.y][self.x+self.speed]
        if self.x-self.speed >0:
            west = astarmap [self.y][self.x-self.speed]
        bestdir = None
        if north <= south and north <= west and north <= east:
            bestdir = "n"
        elif south <= north and south <= west and south <= east: 
            bestdir = "s"
        elif east <= south and east <= west and east <= north:
            bestdir = "e"
        else:
            bestdir = "w"
        if bestdir == "n":
            self.y+=self.speed
        if bestdir == "s":
            self.y-=self.speed
        if bestdir == "e":
            self.x+=self.speed
        if bestdir == "w":
            self.x-=self.speed
       



WORLD_HEIGH = 100
WORLD_WIDTH = 100

def tex_to_sprite(tex):
    return arcade.Sprite(tex, DISPLAY_SCALE)

class Rogue(arcade.Window):
    """
    Main application class.
    """
    def __init__(self):
        self.attacking = False
        self.noclip = False
        self.enemy_hit = False
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

        self.enemies = []
        for i in range (10):
            x,y = self.valid_cord()
            troll = enemy(1,3,"flanker",self.troll_tex,x,y)
            self.enemies.append (troll)
            x,y = self.valid_cord()
            goblin = enemy(1,3,"flanker",self.goblin_tex,x,y)
            self.enemies.append (goblin)
            x,y = self.valid_cord()
            skeleton = enemy(1,3,"flanker",self.skeleton_tex,x,y)
            self.enemies.append (skeleton)        
      
        
    def valid_cord(self):
        x = random.randint(1,WORLD_WIDTH-2)
        y = random.randint(1,WORLD_HEIGH-2)
        while self.level_int [y] [x] != 0:
            x = random.randint(1,WORLD_WIDTH-2)
            y = random.randint(1,WORLD_HEIGH-2)
        return x,y 

    def setup_level(self):
        self.level_int = generate_level(WORLD_WIDTH,WORLD_HEIGH, target_area=500)
        self.wall_tex = self.get_texture("stone1")
        self.other_wall_tex = self.get_texture("stonecorner1")
        self.exit_tex = self.get_texture("exit")
        self.goblin_tex = self.get_texture("goblin")
        self.skeleton_tex = self.get_texture("skeleton")
        self.troll_tex = self.get_texture("troll")
        self.sword_tex = self.get_texture("sword")
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

        self.enemysprite = arcade.SpriteList ()
        for e in self.enemies:
            enemy = tex_to_sprite(e.texture)
            enemy.center_x = (e.x - self.player_x) * TILE_SIZE + SCREEN_WIDTH // 2
            enemy.center_y = (e.y - self.player_y) * TILE_SIZE + SCREEN_HEIGHT // 2
            self.enemysprite.append(enemy)
        self.weaponsprite = arcade.SpriteList ()

        if self.attacking:
        
            weapon_sprite = tex_to_sprite(self.sword_tex)
            self.weaponsprite.append(weapon_sprite)
            weapon_sprite.center_x = (self.weapon_x - self.player_x) * TILE_SIZE + SCREEN_WIDTH // 2
            weapon_sprite.center_y = (self.weapon_y - self.player_y) * TILE_SIZE + SCREEN_HEIGHT // 2
            
    def on_draw(self):
        """ Render the screen. """
        self.clear()
        #self.draw_world_centic()
        self.draw_player_centric()
        self.map_sprites.draw()
        self.player_sprites.draw()
        self.enemysprite.draw()
        self.weaponsprite.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.player_x == self.exit_x and self.player_y == self.exit_y:
            self.gamewin = True
        if self.gamewin:
            print("win")

    def player_attack (self,direction):
        self.attacking = True
        if direction == "up":
            self.weapon_x = self.player_x
            self.weapon_y = self.player_y+1
        if direction == "down":
            self.weapon_x = self.player_x
            self.weapon_y = self.player_y-1
        if direction == "left":
            self.weapon_x = self.player_x-1
            self.weapon_y = self.player_y
        if direction == "right":
            self.weapon_x = self.player_x+1
            self.weapon_y = self.player_y
        if self.level_int[self.weapon_y] [self.weapon_x] !=0:
            self.attacking = False


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

        #attacks 
        if symbol == arcade.key.UP:
            
            x = astar_flood(self.level_int,self.player_x,self.player_y,False)
            self.player_attack("up")
            self.enenemy_attacked()
            for a in self.enemies:
                a.doai(x)
                
        if symbol == arcade.key.DOWN:
            x = astar_flood(self.level_int,self.player_x,self.player_y,False)
            self.player_attack("down")
            self.enenemy_attacked()
            for a in self.enemies:
                a.doai(x)
        if symbol == arcade.key.LEFT:
            x = astar_flood(self.level_int,self.player_x,self.player_y,False)
            self.player_attack("left")
            self.enenemy_attacked()
            for a in self.enemies:
                a.doai(x)
        if symbol == arcade.key.RIGHT:
            x = astar_flood(self.level_int,self.player_x,self.player_y,False)
            self.player_attack("right")
            self.enenemy_attacked()
            for a in self.enemies:
                a.doai(x)

        if self.level_int [newy] [newx] == 0 or self.noclip:
            self.player_x = newx
            self.player_y = newy
            x = astar_flood(self.level_int,self.player_x,self.player_y,False) 
            for a in self.enemies:
                a.doai(x)
            
        if symbol == arcade.key.F:
            self.noclip = not self.noclip

    def enenemy_attacked(self):
        to_remove = []
        for a in self.enemies:
            if a.x == self.weapon_x and a.y == self.weapon_y:
                to_remove.append(a)
        for a in to_remove:
            self.enemies.remove(a)

def main():
    """ Main method"""
    game = Rogue()
    arcade.run()

if __name__ == "__main__":
    main()