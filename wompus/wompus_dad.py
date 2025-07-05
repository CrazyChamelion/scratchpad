# stuff to do next is add add difficulty lvls with functions, easy med hard
# prevent stuff from spawning on player
import random

grid_size = int(input("how big should the map size be? (bigger then 2 )"))
x = 1
y = 1


def point_in_list(l, p_x, p_y):
    for p in l:
        if p_y == p[1] and p_x == p[0]:
            return True
    return False


def get_random_no_overlap_points():
    result = [(1, 1), (1, 2), (2, 1)]  # 1,1 is player initial location
    while len(result) < 7:
        new_y = random.randint(1, grid_size)
        new_x = random.randint(1, grid_size)
        while point_in_list(result, new_x, new_y):
            new_y = random.randint(2, grid_size)
            new_x = random.randint(2, grid_size)
        result.append((new_x, new_y))
    result.remove((1, 1))
    result.remove((1, 2))
    result.remove((2, 1))
    return result


unique_pts = get_random_no_overlap_points()
wompus_x = unique_pts[0][0]
wompus_y = unique_pts[0][1]
bow_x = unique_pts[1][0]
bow_y = unique_pts[1][1]
pit1_x = unique_pts[2][0]
pit1_y = unique_pts[2][1]
pit2_x = unique_pts[3][0]
pit2_y = unique_pts[3][1]

havebow = False
dead_wompus = False


def player_adj_to_pt(px, py):
    return (x == px and (y == py + 1 or y == py - 1)) or (
        y == py and (x == px + 1 or x == px - 1)
    )


def player_on(px, py):
    return x == px and y == py


def death_check():
    if player_on(wompus_x, wompus_y):
        print("the wompus eats you")
        exit()

    if player_on(pit1_x, pit1_y) or player_on(pit2_x, pit2_y):
        print("you fall int a pit and die")
        exit()

    if player_adj_to_pt(wompus_x, wompus_y):
        print("you are next to the wompus")

    if player_adj_to_pt(pit1_x, pit1_y) or player_adj_to_pt(pit2_x, pit2_y):
        print("you are next to the pit")


print(x,y)


def bow_check():
    global havebow
    if player_on(bow_x, bow_y):
        havebow = True
        print("you have a gun, you can defend yourself now")


def get_good_input(prompt):
    move = input(prompt)
    options = ["up", "down", "left", "right"]
    if havebow:
        options.append("shoot")

    while move not in options:
        print(f"{move} is invalid")
        move = input(prompt)
    return move


def shot_hits_wompus(dir_x, dir_y):
    if abs(dir_x) > 1 or abs(dir_y) > 1 or dir_x == dir_y:
        print("invalid programming input fix your stupid code dumbass")
        exit()

    shot_lands_x = x + dir_x
    shot_lands_y = y + dir_y
    return wompus_x == shot_lands_x and wompus_y == shot_lands_y


def direction_to_vector(direction):
    if direction == "up":
        return (0, -1)
    if direction == "down":
        return (0, 1)
    if direction == "right":
        return (1, 0)
    return (-1, 0)


def handle_shot(direction):
    global dead_wompus
    print(f"you shoot the gun {direction}")
    vector = direction_to_vector(direction)
    if shot_hits_wompus(vector[0], vector[1]):
        dead_wompus = True
    else:
        print(
            "you miss the wompus, having wasted yor ammo the wompus hunts you down and eats you, you lose"
        )
        exit()


def position_is_wall(px, py):
    return px == 0 or py == 0 or px == grid_size + 1 or py == grid_size + 1


def move_player(direction):
    global x, y
    vector = direction_to_vector(direction)
    new_x = x + vector[0]
    new_y = y + vector[1]
    if position_is_wall(new_x, new_y):
        print("you run into a wall")
        return
    x = new_x
    y = new_y


def player_turn():
    global y, x, dead_wompus

    prompt = "which way to move? (up,down,left,right) "
    if havebow == True:
        prompt += "(shoot to shoot, range one) "
    move = get_good_input(prompt)

    if havebow == True and move == "shoot":
        direction = input("where do you shoot (up down left right) ")
        handle_shot(direction)

    move_player(move)
    print(x, y)


while True:
    if dead_wompus == True:
        print("You shoot the wompus and win")
        exit()
    if havebow == False:
        bow_check()
    death_check()
    player_turn()
