#stuff to do next is add add difficulty lvls with functions, easy med hard
#prevent stuff from spawning on player
import random
grid_size = int(input("how big should the map size be? (bigger then 2 )"))
x = 1
y = 1
wompus_x = random.randint (1,grid_size)
wompus_y = random.randint (1,grid_size)
bow_x = random.randint (1,grid_size)
bow_y = random.randint (1,grid_size)
pit1_x = random.randint (1,grid_size)
pit1_y = random.randint (1,grid_size)
pit2_x = random.randint (1,grid_size)
pit2_y = random.randint (1,grid_size)
while (wompus_y == bow_y) and (wompus_x == bow_x)  or (wompus_y == pit1_y) and (wompus_x == pit1_x) or (wompus_y == pit2_y) and (wompus_x == pit2_x)  :
    wompus_x = random.randint (1,grid_size)
    wompus_y = random.randint (1,grid_size)

while (pit1_y == pit2_y) and (pit1_x == pit2_x) or (pit1_y == bow_y) and (pit1_x == bow_x) or (pit1_y == wompus_y) and (pit1_x == wompus_x):
    pit1_x = random.randint (1,grid_size)
    pit1_y = random.randint (1,grid_size)
while(pit2_y == bow_y) and (pit2_x == bow_x) or (pit2_y == pit1_y) and (pit2_x == pit1_x) or (pit2_y == wompus_y) and (pit2_x == wompus_x) :
    pit2_x = random.randint (1,grid_size)
    pit2_y = random.randint (1,grid_size)

havebow = False  
dead_wompus = False 

def death_check():
    if  wompus_x == x and (wompus_y == y+1 or wompus_y == y-1): 
        print ("the wompus is next to you")
    elif wompus_y == y and (wompus_x == x+1 or wompus_x == x-1):
        print ("the wompus is next to you")
    elif x == wompus_x and y == wompus_y == y:
        print ("the wompus eats you")
        exit()
    if (pit1_x == x) and (pit1_y == y) or  (pit2_x == x) and (pit2_y == y):
        print ("you fall into a pit and die")
        exit()
    elif  pit1_x == x and (pit1_y == y+1 or pit1_y == y-1) or pit2_x == x and (pit2_y == y+1 or pit2_y == y-1): 
        print ("a pit is next to you")
    elif pit1_y == y and (pit1_x == x+1 or pit1_x == x-1) or  pit2_y == y and (pit2_x == x+1 or pit2_x == x-1):
        print ("a pit is next to you")
   



print ("you are in the top left corner of the map")




def bow_check(): 
            global havebow
            if bow_x == x and bow_y == y:
                havebow = True 
                print ("you have a gun, you can defend yourself now")
    

def wompus_check():
    
        


    if wompus_x == x and wompus_y == y:
        print ("the wompus eats you")
        exit() 

def player_turn(): 
    global y,x, dead_wompus
    
    if havebow == True:
        move = input ("which way to move? (up,down,left,right) (shoot to shoot, range one) ")
    else:
        move = input ("which way to move? (up,down,left,right) ")

    if havebow == True and move == "shoot":
        direction = input("where do you shoot (up down left right) ")
        if direction == "up":
            print ("you shoot the bow up")
            if y -1 == wompus_y and x == wompus_x:
                dead_wompus = True
            else: 
                print ("you miss the wompus, having wasted yor ammo the wompus hunts you down and eats you, you lose")
                exit()
                
        if direction == "down":
            print ("you shoot the bow down")
            if y +1 == wompus_y and x == wompus_x:
                dead_wompus = True
            else: 
                print ("you miss the wompus, having wasted yor ammo the wompus hunts you down and eats you, you lose")
                exit()
        if direction == "right":
            print (" you shoot the bow right")
            if x +1 == wompus_x and y == wompus_y:
                dead_wompus = True
            else: 
                print ("you miss the wompus, having wasted yor ammo the wompus hunts you down and eats you, you lose")
                exit()
        if direction == "left":
            print ("you shoot the bow left")
            if x -1 == wompus_x and y == wompus_y:
                dead_wompus = True
            else: 
                print ("you miss the wompus, having wasted yor ammo the wompus hunts you down and eats you, you lose")
                exit()



    if move == "left":
        x = x-1 
        if x == 0:
            print ("you run into a wall")
            x = 1 

    if move == "right":
        x=x+1
        if x == grid_size+1 :
            print ("you run into a wall")
            x=x-1

    if move == "up":
        y=y-1
        if y == 0:
            print ("you run into a wall")
            y=1
    if move == "down":
        y=y+1
        if y == grid_size +1:
            print ("you run into a wall")
            y=y-1
    print (x,y) 

while True:
    if dead_wompus == True:
        print ("You shoot the wompus and win")
        exit()
    if havebow == False:
        bow_check ()
    death_check()
    player_turn()