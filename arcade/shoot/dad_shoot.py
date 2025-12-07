import arcade
import math
import random
from dataclasses import dataclass

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

def unit_vec(sprite):
        y = math.cos(sprite.radians)
        x = math.sin(sprite.radians)
        return x, y 

def do_physics(sprite, dt):
    sprite.angle += sprite.change_angle *dt

    sprite.center_x += sprite.change_x * dt
    sprite.center_y += sprite.change_y * dt

@dataclass
class ShipKeys:
    up: int
    down: int
    left: int
    right: int
    shoot: int

class Ship():
    def __init__(self, sprite_path, keys, move_speed, turn_rate, bullet_speed):
        self.sprite = arcade.Sprite(sprite_path, 0.5 ,random.randint(50, SCREEN_WIDTH-50),random.randint(50, SCREEN_HEIGHT-50))
        self.bullet_list = arcade.SpriteList()
        self.keys = keys
        self.move_speed = move_speed
        self.turn_rate = turn_rate
        self.bullet_speed = bullet_speed
    
    def shoot(self):
        velocity_x, velocity_y = unit_vec(self.sprite)
        
        path = "./assets/bullet.png"
        bullet =arcade.Sprite(path, 0.1, self.sprite.center_x + velocity_x*self.sprite.width/2, self.sprite.center_y + velocity_y*self.sprite.height/2, )
        bullet.angle = self.sprite.angle +90
        bullet.change_x = velocity_x * self.bullet_speed
        bullet.change_y = velocity_y * self.bullet_speed
        self.bullet_list.append(bullet)

    def on_key_press(self, key):
        match key:
            case self.keys.up:
                vel_x,vel_y = unit_vec(self.sprite)
                self.sprite.change_y = vel_y * self.move_speed
                self.sprite.change_x = vel_x * self.move_speed
            case self.keys.down:
                vel_x,vel_y = unit_vec(self.sprite)
                self.sprite.change_y = -vel_y * self.move_speed
                self.sprite.change_x = -vel_x * self.move_speed
            case self.keys.left:
                self.sprite.change_angle = -self.turn_rate
            case self.keys.right:
                self.sprite.change_angle = self.turn_rate
            case self.keys.shoot:
                self.shoot()

    def on_key_release(self, key):
        match key:
            case self.keys.up | self.keys.down:
                self.sprite.change_y = 0
                self.sprite.change_x = 0
            case self.keys.left | self.keys.right:
                self.sprite.change_angle = 0

    def do_physics(self, dt):
        do_physics(self.sprite, dt)
        for b in self.bullet_list:
            do_physics(b, dt)

    def get_collisions(self, bullets):
        return arcade.check_for_collision_with_list(self.sprite, bullets) 
    
    def looping(self):
        if self.sprite.center_y >=SCREEN_HEIGHT:
            self.sprite.center_y = 50
        if self.sprite.center_y <=0:
            self.sprite.center_y = SCREEN_HEIGHT - 50
        if self.sprite.center_x <=0:
            self.sprite.center_x = SCREEN_WIDTH - 50
        if self.sprite.center_x >=SCREEN_WIDTH:
            self.sprite.center_x = 50

class MyGame(arcade.Window):
    def __init__(self, ):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Shooter")
        self.red_wins = 0
        self.blue_wins = 0
        self.new_game()

    def new_game(self):
        self.blue_hp = 3
        self.red_hp = 3
        self.move_speed = 500
        self.turn_rate = 200
        self.bullet_speed = 400
        
        path = "./assets/07.jpg.webp"
        self.backround = arcade.Sprite(path,3.4,SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.listtomakethebackround = arcade.SpriteList()
        self.listtomakethebackround.append (self.backround) 

        
        self.sprite_list = arcade.SpriteList()
        
        path = "./assets/blue_ship.png"
        self.blue_ship = Ship(path, ShipKeys(up=arcade.key.W, down=arcade.key.S, left=arcade.key.A, right=arcade.key.D, shoot=arcade.key.SPACE), self.move_speed, self.turn_rate, self.bullet_speed)
        self.sprite_list.append (self.blue_ship.sprite) 
        
        path = "./assets/red_ship.png"
        self.red_ship = Ship(path, ShipKeys(up=arcade.key.UP, down=arcade.key.DOWN, left=arcade.key.LEFT, right=arcade.key.RIGHT, shoot=arcade.key.NUM_0), self.move_speed, self.turn_rate, self.bullet_speed)
        self.sprite_list.append (self.red_ship.sprite) 

    def on_key_press(self, key, z):
        self.blue_ship.on_key_press(key)
        self.red_ship.on_key_press(key)
    
    def on_key_release(self, key, z):
        self.blue_ship.on_key_release(key)
        self.red_ship.on_key_release(key)

    def looping (self):
        self.red_ship.looping()
        self.blue_ship.looping()
        
    def game_end(self):
        if self.blue_hp <=0:
            print ("red wins") 
            self.red_wins += 1 
            print (f"red has won {self.red_wins} time(s) blue has won {self.blue_wins} time(s)")
            self.new_game ()
        if self.red_hp <=0:
            print ("blue wins") 
            self.blue_wins += 1 
            print (f"red has won {self.red_wins} time(s) blue has won {self.blue_wins} time(s)")
            self.new_game ()

    def draw_health(self):
        for x in range(self.red_hp):
            arcade.draw.draw_circle_filled((x + 1)*30, SCREEN_HEIGHT-20, 10, arcade.color.RED)

        for x in range(self.blue_hp):
            arcade.draw.draw_circle_filled(SCREEN_WIDTH-(x + 1)*30, SCREEN_HEIGHT-20, 10, arcade.color.BLUE)

    def on_draw(self):
        self.clear()
        self.listtomakethebackround.draw()
        self.sprite_list.draw()
        self.blue_ship.bullet_list.draw()
        self.red_ship.bullet_list.draw()
        self.draw_health()

    def do_physics(self, dt):
        self.blue_ship.do_physics(dt)
        self.red_ship.do_physics(dt)
        

    def on_update(self, dt):
        self.do_physics(dt)
        self.looping()
        self.game_end() 
        
        red_bullet_hit_list = self.red_ship.get_collisions(self.blue_ship.bullet_list)
        for rbullet in red_bullet_hit_list: 
            rbullet.remove_from_sprite_lists()
            self.red_ship.center_x = random.randint(0,SCREEN_WIDTH) 
            self.red_ship.center_y = random.randint(0,SCREEN_HEIGHT) 
            self.blue_ship.center_x = random.randint(0,SCREEN_WIDTH) 
            self.blue_ship.center_y = random.randint(0,SCREEN_HEIGHT) 
            self.red_hp -= 1
            
        blue_bullet_hit_list = self.blue_ship.get_collisions(self.red_ship.bullet_list)
        for bbullet in blue_bullet_hit_list: 
            bbullet.remove_from_sprite_lists()
            self.blue_ship.center_x = random.randint(0,SCREEN_WIDTH) 
            self.blue_ship.center_y = random.randint(0,SCREEN_HEIGHT) 
            self.red_ship.center_x = random.randint(0,SCREEN_WIDTH) 
            self.red_ship.center_y = random.randint(0,SCREEN_HEIGHT) 
            self.blue_hp -= 1
           
def main():
    window = MyGame()
    arcade.run()        

if __name__ == "__main__":
    main()