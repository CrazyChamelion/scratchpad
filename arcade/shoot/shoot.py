import arcade
import math
import random
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000


class MyGame(arcade.Window):
    def __init__(self, ):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Shooter")
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
        self.bullet_list = arcade.SpriteList ()

        self.physics_engines = [arcade.PhysicsEngineSimple(self.blue_ship), arcade.PhysicsEngineSimple(self.red_ship)]
        
    def shoot_bullet(self, ship):
        velocity_x, velocity_y = self.unit_vec(ship)
        
        path = "./assets/bullet.png"
        bullet =arcade.Sprite(path, 0.1, ship.center_x + velocity_x*ship.width/2, ship.center_y + velocity_y*ship.height/2, )
        bullet.angle = ship.angle +90
        bullet.change_x = velocity_x * self.bullet_speed
        bullet.change_y = velocity_y * self.bullet_speed
        self.physics_engines.append(arcade.PhysicsEngineSimple(bullet))
        self.bullet_list.append (bullet)

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
            self.shoot_bullet(self.blue_ship)

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
            self.shoot_bullet(self.red_ship)
    
    def on_key_release(self, key, z):
        if key == arcade.key.W or key == arcade.key.S:
            self.blue_ship.change_y = 0
            self.blue_ship.change_x = 0

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.red_ship.change_y = 0
            self.red_ship.change_x = 0
        if key == arcade.key.A or key == arcade.key.D:
            self.blue_ship.change_angle = 0
        if key == arcade.key.LEFT or arcade.key.RIGHT:
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
        
        


    def on_draw(self):
        
        self.clear()
        self.listtomakethebackround.draw()
        self.sprite_list.draw()
        self.bullet_list.draw()
    def on_update(self, x):
        for e in self.physics_engines:
            e.update()
        self.looping()
def main():
    window = MyGame()
    arcade.run()        

if __name__ == "__main__":
    main()