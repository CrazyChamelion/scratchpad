""" Chess Program """

import arcade
from enum import Enum

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SQUARE = SCREEN_HEIGHT / 8

class Coordinate:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def ToXY(self ):
        return self.i * SQUARE + SQUARE / 2 , self.j * SQUARE + SQUARE / 2
    
class Direction(Enum):
    UP = 1
    DOWN = 2

class Color(Enum):
    WHITE = 1
    BLACK = 2

class Type(Enum):
    KING = 1
    QUEEN = 2
    ROOK = 3
    BISHOP = 4
    KNIGHT = 5
    PAWN = 6

def init_sprite (sprite, cord):
    sprite.width = SQUARE
    sprite.height = SQUARE
    sprite.center_x , sprite.center_y = cord.ToXY()
    return sprite 

class Piece():
    def __init__(self, type, color, dir , cord):
        self.type = type
        self.color = color
        self.dir = dir
        self.cord = cord
        self.init_sprite()

    def init_sprite(self):
        path = "./assets/"
        match self.color:
            case Color.WHITE:
                path += "white"
            case Color.BLACK:
                path += "black"

        path += "-"

        match self.type:
            case Type.PAWN:
                path += "pawn"
            case Type.KNIGHT:
                path += "knight"
            case Type.BISHOP:
                path += "bishop"
            case Type.ROOK:
                path += "rook"
            case Type.QUEEN:
                path += "queen"
            case Type.KING:
                path += "king"
            
        path += ".png"
        self.sprite = init_sprite(arcade.Sprite(path), self.cord)


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Chess")
        # 30, 30 top left. Used 30 to leave room for the windows controls
        self.set_location(0, 30)
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.reset_board()
        self.clicked_on = False

    def reset_board(self):
        self.sprite_list = arcade.SpriteList()
        self.pieces = []
        # makes pawns
        for col in range(8):
            piece = Piece(Type.PAWN, Color.WHITE, Direction.UP, Coordinate(col, 1))
            self.sprite_list.append(piece.sprite)
            self.pieces.append(piece)
        
            piece = Piece (Type.PAWN , Color.BLACK, Direction.DOWN, Coordinate(col, 6))
            self.sprite_list.append(piece.sprite)
            self.pieces.append(piece)
        
        rook = 0
        knight = 1
        bishop = 2 

        for i in range(2):
            # rooks
            piece = Piece(Type.ROOK, Color.WHITE, Direction.UP, Coordinate(rook, 0))
            self.sprite_list.append(piece.sprite)
            self.pieces.append(piece)
            
            piece = Piece(Type.ROOK, Color.BLACK, Direction.DOWN, Coordinate(rook, 7))
            self.sprite_list.append(piece.sprite)
            self.pieces.append(piece)
            rook=rook+7
            #knights
            piece = Piece(Type.KNIGHT, Color.WHITE, Direction.UP, Coordinate(knight, 0))
            self.sprite_list.append(piece.sprite)
            self.pieces.append(piece)
            
            piece = Piece(Type.KNIGHT, Color.BLACK, Direction.DOWN, Coordinate(knight, 7))
            self.sprite_list.append(piece.sprite)
            self.pieces.append(piece)
            knight = knight + 5
            #bishop
            piece = Piece(Type.BISHOP, Color.WHITE, Direction.UP, Coordinate(bishop, 0))
            self.sprite_list.append(piece.sprite)
            self.pieces.append(piece)
            
            piece = Piece(Type.BISHOP, Color.BLACK, Direction.DOWN, Coordinate(bishop, 7))
            self.sprite_list.append(piece.sprite)
            self.pieces.append(piece)
            bishop = bishop + 3 

        #king
        piece = Piece(Type.KING, Color.WHITE, Direction.UP, Coordinate(3, 0))
        self.sprite_list.append(piece.sprite)
        self.pieces.append(piece)
            
        piece = Piece(Type.KING, Color.BLACK, Direction.DOWN, Coordinate(3, 7))
        self.sprite_list.append(piece.sprite)
        self.pieces.append(piece)
        #queen
        piece = Piece(Type.QUEEN, Color.WHITE, Direction.UP, Coordinate(4, 0))
        self.sprite_list.append(piece.sprite)
        self.pieces.append(piece)
            
        piece = Piece(Type.QUEEN, Color.BLACK, Direction.DOWN, Coordinate(4, 7))
        self.sprite_list.append(piece.sprite)
        self.pieces.append(piece)
         
    def on_draw(self):
        self.clear()
        self.draw_grid()
        self.sprite_list.draw()

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

    def find_clicked_piece(self, x, y):
        return 0

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT :
            print (x,y)
            
    
    
def main():
    window = MyGame()
    arcade.run()


if __name__ == "__main__":
    main()