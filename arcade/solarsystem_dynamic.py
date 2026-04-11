import arcade
import math
from enum import Enum
import time 
# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Solar System"

SUNX = SCREEN_WIDTH//2
SUNY = SCREEN_HEIGHT//2

SOLAR_MASS = 1
G = 39.5
DT = 0.001

class Orbit(Enum):
    ELIPSE = 1
    CIRCLE = 2
    PARABILIC = 3
    HYPERBOLIC = 4


def autp(au):
    # make mars at 1.5 au take up most of the screen
    return au*(SCREEN_WIDTH//2 - 50)/1.5 # mars is outer
    #return au*(SCREEN_WIDTH//2 - 50)/10 # zoomed out

class Planet():
    def __init__(self, r_o, r_p, m, c, obt):
        self.r_o = r_o
        self.r_p = r_p
        self.m = m
        self.c = c
        self.x = self.r_o
        self.y = 0
        self.vx = 0 

        if obt == Orbit.ELIPSE:
            self.vy = math.sqrt((G*SOLAR_MASS)/self.r_o) 
            self.vy *= 0.8
        elif obt == Orbit.CIRCLE:
            self.vy = math.sqrt((G*SOLAR_MASS)/self.r_o)
        elif obt == Orbit.PARABILIC:
            self.vx = -math.sqrt((2 * G * SOLAR_MASS) / self.r_o)
            self.vy = self.r_o*2
            self.x = self.r_o*8
        else:
            # hyperbolic
            self.vx = -math.sqrt((2 * G * SOLAR_MASS) / self.r_o) * 1.2
            self.vy = 0
            self.vy = self.r_o*2
            self.x = self.r_o*8
        
        self.old_pos = [(SUNX + autp(self.x), SUNY + autp(self.y))]
        self.pas_track_counter = 0
        self.angle_traversed = 0

        # make it go to fast
        #self.vy *=10

    def update(self):
        r = math.sqrt(self.x**2 + self.y**2)
        f = ((G*SOLAR_MASS*self.m)/r**2) *-1 
        theta = math.atan2(self.y, self.x)
        fx = f * (self.x / r)
        fy = f * (self.y / r)
        ax = fx/self.m
        ay = fy/self.m
        self.vx +=ax*DT
        self.vy += ay*DT
        self.x +=self.vx*DT
        self.y +=self.vy*DT

        self.pas_track_counter +=1
        new_theta = math.atan2(self.y, self.x)
        dtheta = new_theta - theta
        # Wrap into [-pi, pi]
        if dtheta > math.pi:
            dtheta -= 2 * math.pi
        elif dtheta < -math.pi:
            dtheta += 2 * math.pi
        self.angle_traversed += abs(dtheta)
        
        if self.angle_traversed > 6*math.pi:
            self.old_pos.clear()
            self.angle_traversed = 0
        if self.pas_track_counter % 10 == 0:
            print(self.angle_traversed)
            self.old_pos.append((SUNX + autp(self.x), SUNY + autp(self.y)))

    def draw(self):
        # current position
        arcade.draw_circle_filled(SUNX + autp(self.x), SUNY + autp(self.y), self.r_p, self.c)
        # circular orbit
        arcade.draw_circle_outline(SUNX,SUNY,autp(self.r_o),arcade.color.NEON_FUCHSIA)
        # the actual orbit
        arcade.draw_line_strip(self.old_pos, arcade.color.ORANGE)

class MyGame(arcade.Window):
    """
    Main application class.
    """
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.plannets = []
        # mercury
        self.plannets.append(Planet(0.387, 10, 1.66e-7, arcade.color.RED, Orbit.CIRCLE))
        # venus
        self.plannets.append(Planet(0.722, 10, 2.45e-6, arcade.color.LIGHT_BLUE, Orbit.CIRCLE))
        # earth
        self.plannets.append(Planet(1, 10, 3e-6, arcade.color.BLUE, Orbit.CIRCLE))
        # mars
        self.plannets.append(Planet(1.52, 10, 3.23e-7, arcade.color.ORANGE, Orbit.CIRCLE))
        self.petx = 0
        self.pety = 0

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        # Drawing plannets
        for p in self.plannets:
            p.draw()
        # sun
        arcade.draw_circle_filled(SUNX,SUNY,30,arcade.color.YELLOW) 
        #arcade.draw_circle_filled(SUNX,SUNY,3,arcade.color.YELLOW) 
        self.petrova_d()

    def petrova_d(self):
            arcade.draw_circle_filled(autp(self.petx)+SUNX,autp(self.pety)+SUNY,10,arcade.color.BLUE)
            

    def petrova_u(self):
        venus = self.plannets[1]
        dx = venus.x - self.petx 
        dy = venus.y - self.pety 
        len = math.sqrt((dx**2 + dy**2 ))
        if len <0.001:
            self.petx = 0 
        dx = dx / len
        dy = dy / len
        petvel = 0.01
        self.petx += petvel * dx
        self.pety += petvel * dy
    
            

    def on_update(self, delta_time):
        """ Movement and game logic """
        for p in self.plannets:
            p.update()
        self.petrova_u()

def main():
    """ Main method"""
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
