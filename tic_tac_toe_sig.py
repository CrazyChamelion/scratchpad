one = " "
two = " "
three = " "
four = " "
five = " " 
six = " "
seven = " " 
eight = " " 
nine = " "
def board():
    print ("|", one ,  "|", two , "|",three, "|")
    print ("-------------")
    print("|", four, "|" , five, "|", six, "|")
    print ("-------------")
    print("|", seven, "|", eight, "|", nine, "|")

def game_loop():
    global one, two, three, four, five, six, seven, eight, nine
    board ()
    x = input ("where would you like to place an X? (one is the top left nine is the bottem right) ")
    
    
    if x == "one":
        one = "X"
    if x == "two":
        two = "X"
    if x == "three":
        three = "X"
    if x == "four": 
        four = "X"
    if x == "five": 
        five = "X"
    if x == "six": 
        six = "X"
    if x == "seven":
        seven = "X"
    if x == "eight":
        eight = "X"
    if x == "nine":
        nine = "X"
    
    board()
    if game_is_draw():
        return
    if player_wins("X"):
        return
    
    y = input ("where would you like to place an O? (one is the top left nine is the bottem right) ")
    
    if y == "one": 
        one = "O"
    if y == "two":
        two = "O"
    if y == "three":
        three = "O"
    if y == "four":
        four = "O"
    if y == "five":
        five = "O"
    if y == "six": 
        six = "O"
    if y == "seven":
        seven = "O"
    if y == "eight":
        eight = "O"
    if y == "nine":
        nine = "O"
        

def game_is_draw():
    return one != " " and two != " " and three != " " and four != " " and five != " " and six != " " and seven != " " and eight != " " and nine != " "

def player_wins(p):
    return one == p and two == p and three == p or \
        four == p and five == p and six == p or \
        seven == p and eight == p and nine == p or \
        one == p and four == p and seven == p or \
        two == p and five == p and eight == p or \
        three == p and six == p and nine == p or \
        one == p and five == p and nine == p or \
        three == p and five == p and seven == p


print(game_is_draw())
while not game_is_draw():
    game_loop()
    if player_wins("X"):
        print("X wins")
        break
    if player_wins("O"):
        print("O wins")
        break