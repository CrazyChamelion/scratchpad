import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class ai_player():
    def __init__(self, sprite, score_x, score_y):
        self.sprite = sprite
        self.score = 0
        self.score_x = score_x
        self.score_y = score_y

    def draw_score(self):
        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, self.score_x, self.score_y, arcade.color.BLACK, 14)

    def check_coin_hit(self, coin_list):
        # Generate a list of all sprites that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(self.sprite, coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            self.score += 1

        return coins_hit_list
    
    def move(self):
        pass

class sweeper(ai_player):
    def __init__(self, sprite, score_x, score_y):
        super().__init__(sprite, score_x, score_y)
        self.right = True
        self.up = True

    def move(self):
        if self.sprite.center_y >= SCREEN_HEIGHT:
            self.up = False
            self.sprite.center_y -= 10
        if self.sprite.center_y <= 0:
            self.up = True
            self.sprite.center_y += 10
        if self.right:
            self.sprite.center_x += 20
            if self.sprite.center_x >= SCREEN_WIDTH:
                self.right = False
                if self.up: 
                    self.sprite.center_y += self.sprite.height 
                else:
                    self.sprite.center_y -= self.sprite.height 
        else:
            self.sprite.center_x -= 20
            if self.sprite.center_x <= 0:
                self.right = True
                if self.up: 
                        self.sprite.center_y += self.sprite.height
                else:
                        self.sprite.center_y -= self.sprite.height

class jumper(ai_player):
    def __init__(self, sprite, score_x, score_y):
        super().__init__(sprite, score_x, score_y)
    
    def move(self):
        self.sprite.center_x = random.randrange(SCREEN_WIDTH)
        self.sprite.center_y = random.randrange(SCREEN_HEIGHT)



class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Collisions")

        # Variables that will hold sprite lists.
        self.player_list = None
        self.coin_list= None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        self.ai_players = []

        # Don't show the mouse cursor
        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the players
        s1_sprite = arcade.Sprite("character.png", SPRITE_SCALING_PLAYER)
        s1_sprite.center_x = 50
        s1_sprite.center_y = 50
        self.player_list.append(s1_sprite)
        s1 = sweeper(s1_sprite, 10, 40)
        self.ai_players.append(s1)

        s2_sprite = arcade.Sprite("character.png", SPRITE_SCALING_PLAYER)
        s2_sprite.center_x = SCREEN_WIDTH - 50
        s2_sprite.center_y = SCREEN_HEIGHT - 50
        self.player_list.append(s2_sprite)
        s2 = jumper(s2_sprite, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40)
        self.ai_players.append(s2)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite("coin_01.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            

            # Add the coin to the lists
            self.coin_list.append(coin)
 
    def on_draw(self):
        self.clear()

        # Draw the sprite lists here. Typically sprites are divided into
        # different groups. Other game engines might call these "sprite layers"
        # or "sprite groups." Sprites that don't move should be drawn in their
        # own group for the best performance, as Arcade can tell the graphics
        # card to just redraw them at the same spot.
        # Try to avoid drawing sprites on their own, use a SpriteList
        # because there are many performance improvements in that code.
        self.coin_list.draw()
        self.player_list.draw()

        for p in self.ai_players:
            p.draw_score()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()
        for p in self.ai_players:
            p.move()
            p.check_coin_hit(self.coin_list)



def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
    