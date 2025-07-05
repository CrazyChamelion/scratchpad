board = [[" "]*3, [" "]*3, [" "]*3]

def print_board(b):
    print("-"*7)
    for x in b:
        row = "|"
        for ch in x:
            row += ch + "|"
        print(row)
        print("-"*7)

def do_move(p, b):
    x = 10
    y = 10
    while True:
        raw_move = input(f"enter move for {p} as x y where x and y are numbers between 0 and 2 ")
        parts = raw_move.split(" ")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit:
            x = int(parts[0])
            y = int(parts[1])
            if x >= 0 and x < 3 and y >= 0 and y < 3:
                if b[y][x] != " ":
                    print("space is taken")
                else:
                    break
        print("input conditions not met. try again")
    b[y][x] = p

def all_places_are_symbol(symbol, places, board):
    for p in places:
        if board[p[1]][p[0]] != symbol:
            return False
    return True

def player_won(p, b):
    wins = [[(0, 0), (0, 1), (0, 2)], \
            [(1, 0), (1, 1), (1, 2)], \
            [(2, 0), (2, 1), (2, 2)], \
            [(0, 0), (1, 0), (2, 0)], \
            [(0, 1), (1, 1), (1, 1)], \
            [(0, 2), (1, 2), (2, 2)], \
            [(0, 0), (1, 1), (2, 2)], \
            [(2, 0), (1, 1), (0, 2)]]
    for win in wins:
        if all_places_are_symbol(p, win, b):
            return True
    return False

def is_a_draw(b):
    for row in b:
        for letter in row:
            if letter == " ":
                return False
    return True

player = "X" 
while True:
    print_board(board)
    do_move(player, board)
    if player_won(player, board):
        print_board(board)
        print(f"{player} won")
        break
    
    if is_a_draw(board):
        print_board(board)
        print("its a draw")
        break

    if player == "X":
        player = "O"
    else:
        player = "X"