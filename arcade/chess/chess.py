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
    
    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def toXY(self ):
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
    sprite.center_x , sprite.center_y = cord.toXY()
    return sprite 

class Piece():
    def __init__(self, type, color, dir , cord):
        self.type = type
        self.color = color
        self.dir = dir
        self.cord = cord
        self.init_sprite()
        self.isfirstmove = True

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

    def move_to(self, coord):
        self.cord = coord
        self.sprite.center_x, self.sprite.center_y = coord.toXY()
    
    def get_moves(self, pieces):
        
        result = []
        if self.type == Type.ROOK:
            print ("a rook was clicked")
            for a in range (10):
                result.append(Coordinate(self.cord.i +a , self.cord.j))
                result.append(Coordinate(self.cord.i -a , self.cord.j))
                result.append(Coordinate(self.cord.i  , self.cord.j+a))
                result.append(Coordinate(self.cord.i  , self.cord.j-a))
        elif self.type == Type.BISHOP: 
            print ("a bishop was clicked")
            for a in range (10):
                result.append(Coordinate(self.cord.i +a , self.cord.j+a))
                result.append(Coordinate(self.cord.i -a , self.cord.j-a))
                result.append(Coordinate(self.cord.i -a , self.cord.j+a))
                result.append(Coordinate(self.cord.i +a , self.cord.j-a))
        elif self.type == Type.KNIGHT: 
            print ("a knight was clicked")
            result.append(Coordinate(self.cord.i +2 , self.cord.j+1))
            result.append(Coordinate(self.cord.i +2 , self.cord.j-1))
            result.append(Coordinate(self.cord.i +1 , self.cord.j+2))
            result.append(Coordinate(self.cord.i +1 , self.cord.j-2))
            result.append(Coordinate(self.cord.i -2 , self.cord.j+1))
            result.append(Coordinate(self.cord.i -2 , self.cord.j-1))
            result.append(Coordinate(self.cord.i -1 , self.cord.j+2))
            result.append(Coordinate(self.cord.i -1 , self.cord.j-2))
        elif self.type == Type.KING:
            print ("a king was clicked")
            result.append(Coordinate(self.cord.i +1 , self.cord.j+1))
            result.append(Coordinate(self.cord.i -1 , self.cord.j-1))
            result.append(Coordinate(self.cord.i +1 , self.cord.j-1))
            result.append(Coordinate(self.cord.i -1 , self.cord.j+1))
            result.append(Coordinate(self.cord.i , self.cord.j+1))
            result.append(Coordinate(self.cord.i , self.cord.j-1))
            result.append(Coordinate(self.cord.i +1 , self.cord.j))
            result.append(Coordinate(self.cord.i -1 , self.cord.j))
        elif self.type == Type.QUEEN:
            print ("a queen was clicked")
            for a in range (10):
                result.append(Coordinate(self.cord.i +a , self.cord.j))
                result.append(Coordinate(self.cord.i -a , self.cord.j))
                result.append(Coordinate(self.cord.i  , self.cord.j+a))
                result.append(Coordinate(self.cord.i  , self.cord.j-a)) 
                result.append(Coordinate(self.cord.i +a , self.cord.j+a))
                result.append(Coordinate(self.cord.i -a , self.cord.j-a))
                result.append(Coordinate(self.cord.i -a , self.cord.j+a))
                result.append(Coordinate(self.cord.i +a , self.cord.j-a))
        elif self.type == Type.PAWN:
            if self.dir == Direction.UP:
                z = +1 
            else:
                z = -1               
            if self.isfirstmove == True: 
                result.append(Coordinate(self.cord.i  , self.cord.j+2* z ))      
            result.append(Coordinate(self.cord.i  , self.cord.j+ z )) 
            
            # look for captures
            forward = 1
            if self.color == Color.BLACK:
                forward = -1
            for p in pieces:
                capturedi = p.cord.i 
                capturedj = p.cord.j
                if self.cord.j+forward == capturedj and self.cord.i == capturedi:
                    result.remove (Coordinate(capturedi,capturedj))
                if self.cord.j + forward == capturedj and (self.cord.i +1 == capturedi or self.cord.i -1 == capturedi):
                    result.append(Coordinate(capturedi, capturedj))
            print ("a pawn was clicked")
        else:
            print ("SHIT SHIT SHIT SHIT SHIT ITS FUCKED ITS FUCKED ITS FUCKED")
            raise Exception("Unknown piece type was cliced")
        
        # remove moves off the board
        for r in result:
            if r.i < 0 or r.j < 0 or r.i > 7 or r.j > 7:
                result.remove(r)
        
        # handle diagonal moving through pieces for bishop and queen
        if self.type == Type.QUEEN or self.type == Type.BISHOP:
            for p in pieces:
                if self.cord.i == p.cord.i and self.cord.j == p.cord.j:
                    # this piece is self
                    continue

                deltai = p.cord.i - self.cord.i
                deltaj = p.cord.j - self.cord.j
                if abs(deltai) != abs(deltaj):
                    # piece p is not on a diagonal with self
                    continue
                di = 1
                if deltai < 0:
                    di = -1
                dj = 1
                if deltaj < 0:
                    dj = -1
                start = 0
                if p.color != self.color:
                    start = 1
                for a in range(start, 7):
                    to_remove = Coordinate(p.cord.i + a*di, p.cord.j + a*dj)
                    if to_remove in result:
                        result.remove(to_remove)
                

        # handle rook and queen moving through pieces horizontal or verticle
        if self.type == Type.QUEEN or self.type == Type.ROOK:
            for p in pieces:
                # horizontal
                if p.cord.j == self.cord.j:
                    if p.cord.i == self.cord.i:
                        # same piece
                        continue
                    else:
                        stop = 8
                        dir = 1
                        start = int(p.cord.i)
                        if p.cord.i < self.cord.i:
                            stop = -1
                            dir = -1
                        if p.color != self.color:
                            start += dir
                        # remove p and also remove any square left of p
                        for a in range(start, stop, dir):
                            to_remove = Coordinate(a, self.cord.j)
                            if to_remove in result:
                                result.remove(to_remove)
                # verticle
                if p.cord.i == self.cord.i:
                    if p.cord.j == self.cord.j:
                        # same piece
                        continue
                    else:
                        stop = 8
                        dir = 1
                        start = int(p.cord.j)
                        if p.cord.j < self.cord.j:
                            stop = -1
                            dir = -1
                        if p.color != self.color:
                            start += dir
                        # remove p and also remove any square left of p
                        for a in range(start, stop, dir):
                            to_remove = Coordinate(self.cord.i, a)
                            if to_remove in result:
                                result.remove(to_remove)
                    

        # prevent moves that land on color
        for p in pieces: 
            if p.color != self.color:
                continue
            piecei = p.cord.i  
            piecej = p.cord.j
            for r in result:
                if r.j == piecej and r.i == piecei:
                    result.remove(r) 
                
                
        return result


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Chess")
        # 30, 30 top left. Used 30 to leave room for the windows controls
        self.set_location(0, 30)
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.reset_board()
        self.clicked_on = False
        

    def reset_board(self):
        self.pos_moves = []
        self.selected_piece = None
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
        if self.selected_piece: 
            arcade.draw_rect_filled(arcade.rect.XYWH((self.selected_piece.cord.i + 0.5) *SQUARE , (self.selected_piece.cord.j +0.5) * SQUARE , SQUARE , SQUARE ),arcade.color.RED)
        for move in self.pos_moves:
            arcade.draw_rect_filled(arcade.rect.XYWH((move.i + 0.5) *SQUARE , (move.j +0.5) * SQUARE , SQUARE , SQUARE ),arcade.color.RED)
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

    def on_key_press (self, key, modifiers ):
        if key == arcade.key.ESCAPE:
            self.clicked_on = False 
            self.pos_moves.clear()
            self.selected_piece = None      

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT :
            print (x,y)
            square_click_x = x // SQUARE
            square_click_y = y // SQUARE 
            print (square_click_x, square_click_y)
            #if clicked on piece last time
            if self.selected_piece:
                for move in self.pos_moves:
                    if square_click_x == move.i and square_click_y == move.j:  
                        self.selected_piece.move_to(Coordinate(square_click_x, square_click_y))
                        self.pos_moves.clear()
                        # check for capture
                        for p in self.pieces:
                            capturedi = p.cord.i 
                            capturedj = p.cord.j
                            if (move.i == capturedi and move.j == capturedj) and p != self.selected_piece: 
                                self.pieces.remove (p)
                                self.sprite_list.remove(p.sprite)
                                break
                        self.selected_piece.isfirstmove = False 
                        
                        #promote
                        if self.selected_piece.type == Type.PAWN: 
                            if move.j == 0 or move.j == 7: 
                                self.pieces.remove (self.selected_piece)
                                self.sprite_list.remove (self.selected_piece.sprite)
                                piece = Piece(Type.QUEEN, self.selected_piece.color, self.selected_piece.dir, Coordinate(self.selected_piece.cord.i, self.selected_piece.cord.j))
                                self.sprite_list.append(piece.sprite)
                                self.pieces.append(piece)
                        self.selected_piece = None
                                                                            #click on piece first time
            else:
                for piece in self.pieces:
                    if square_click_x == piece.cord.i and square_click_y == piece.cord.j: 
                            self.selected_piece = piece
                            self.pos_moves = piece.get_moves(self.pieces)
                            
    
def main():
    window = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()