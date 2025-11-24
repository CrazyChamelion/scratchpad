import arcade
import math
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000


class MyGame(arcade.Window):
    def __init__(self, ):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Shooter")
        self.red_wins = 0
        self.blue_wins = 0
        self.new_game()

    def new_game(self):
        self.blue_hp = 3
        self.red_hp = 3
        self.move_speed = 10
        self.turn_rate = 5
        self.bullet_speed = 20
        path = "./assets/07.jpg.webp"
        self.backround = arcade.Sprite(path,3.4,SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.listtomakethebackround = arcade.SpriteList()
        self.listtomakethebackround.append (self.backround) 
        path = "./assets/blue_ship.png"
        self.sprite_list = arcade.SpriteList()
        self.blue_ship = arcade.Sprite(path, 0.5 ,random.randint(50, SCREEN_WIDTH-50),random.randint(50, SCREEN_HEIGHT-50))
        self.sprite_list.append (self.blue_ship) 
        path = "./assets/red_ship.png"
        self.red_ship = arcade.Sprite(path, 0.5 , random.randint(50, SCREEN_WIDTH-50),random.randint(50, SCREEN_HEIGHT-50))
        self.sprite_list.append (self.red_ship) 
        self.bbullet_list = arcade.SpriteList ()
        self.rbullet_list = arcade.SpriteList ()

        self.physics_engines = [arcade.PhysicsEngineSimple(self.blue_ship), arcade.PhysicsEngineSimple(self.red_ship)]
        
    def shoot_bullet(self, ship,list ):
        velocity_x, velocity_y = self.unit_vec(ship)
        
        path = "./assets/bullet.png"
        bullet =arcade.Sprite(path, 0.1, ship.center_x + velocity_x*ship.width/2, ship.center_y + velocity_y*ship.height/2, )
        bullet.angle = ship.angle +90
        bullet.change_x = velocity_x * self.bullet_speed
        bullet.change_y = velocity_y * self.bullet_speed
        self.physics_engines.append(arcade.PhysicsEngineSimple(bullet))
        list.append (bullet)

    def on_key_press(self, key, z):
        if key == arcade.key.W:
            vel_x,vel_y = self. unit_vec(self.blue_ship)
            self.blue_ship.change_y = vel_y * self.move_speed
            self.blue_ship.change_x = vel_x * self.move_speed
            
        if key == arcade.key.S:
            vel_x,vel_y = self. unit_vec(self.blue_ship)
            self.blue_ship.change_y = -vel_y * self.move_speed
            self.blue_ship.change_x = -vel_x * self.move_speed
            
        if key == arcade.key.A:
            self.blue_ship.change_angle = -self.turn_rate
        if key == arcade.key.D:
            self.blue_ship.change_angle = self.turn_rate

        if key == arcade.key.CAPSLOCK:
            self.shoot_bullet(self.blue_ship,self.bbullet_list)

        if key == arcade.key.UP:
            vel_x,vel_y = self. unit_vec(self.red_ship)
            self.red_ship.change_y = vel_y * self.move_speed
            self.red_ship.change_x = vel_x * self.move_speed
            
        if key == arcade.key.DOWN:
            vel_x,vel_y = self. unit_vec(self.red_ship)
            self.red_ship.change_y = -vel_y * self.move_speed
            self.red_ship.change_x = -vel_x * self.move_speed
        if key == arcade.key.LEFT:
            self.red_ship.change_angle = -self.turn_rate
        if key == arcade.key.RIGHT:
            self.red_ship.change_angle = self.turn_rate

        if key == arcade.key.NUM_0:
            self.shoot_bullet(self.red_ship,self.rbullet_list)
    
    def on_key_release(self, key, z):
        if key == arcade.key.W or key == arcade.key.S:
            self.blue_ship.change_y = 0
            self.blue_ship.change_x = 0

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.red_ship.change_y = 0
            self.red_ship.change_x = 0
        if key == arcade.key.A or key == arcade.key.D:
            self.blue_ship.change_angle = 0
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.red_ship.change_angle = 0
        
    def unit_vec(self, sprite):
        y = math.cos(sprite.radians)
        x = math.sin(sprite.radians)
        return x, y 

    def looping (self):
        if self.blue_ship.center_y >=SCREEN_HEIGHT:
            self.blue_ship.center_y = 50
        if self.blue_ship.center_y <=0:
            self.blue_ship.center_y = SCREEN_HEIGHT - 50
        if self.blue_ship.center_x <=0:
            self.blue_ship.center_x = SCREEN_WIDTH - 50
        if self.blue_ship.center_x >=SCREEN_WIDTH:
            self.blue_ship.center_x = 50

        if self.red_ship.center_y >=SCREEN_HEIGHT:
            self.red_ship.center_y = 50
        if self.red_ship.center_y <=0:
            self.red_ship.center_y = SCREEN_HEIGHT - 50
        if self.red_ship.center_x >=SCREEN_WIDTH:
            self.red_ship.center_x = 50
        if self.red_ship.center_x <=0:
            self.red_ship.center_x = SCREEN_WIDTH - 50
        
    
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
        self.bbullet_list.draw()
        self.rbullet_list.draw()
        self.draw_health()

    def on_update(self, x):
        for e in self.physics_engines:
            e.update()
        self.looping()
        self.game_end() 
        
        red_bullet_hit_list = arcade.check_for_collision_with_list(self.red_ship, self.bbullet_list) 
        for rbullet in red_bullet_hit_list: 
            rbullet.remove_from_sprite_lists()
            self.red_ship.center_x = random.randint(0,SCREEN_WIDTH) 
            self.red_ship.center_y = random.randint(0,SCREEN_HEIGHT) 
            self.blue_ship.center_x = random.randint(0,SCREEN_WIDTH) 
            self.blue_ship.center_y = random.randint(0,SCREEN_HEIGHT) 
            self.red_hp -= 1
            
           
            
        blue_bullet_hit_list = arcade.check_for_collision_with_list(self.blue_ship, self.rbullet_list) 
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