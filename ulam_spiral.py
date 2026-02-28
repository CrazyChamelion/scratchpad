from termcolor import colored, cprint

def get_grid(size):
    return  [[0 for _ in range(size)] for _ in range(size)]

def sieve_of_eratosthenes(max):
    candidates = [True]*max
    candidates[0] = False
    for i in range(1, max):
        if not candidates[i]:
            continue
        num = i + 1
        for j in range(i + num, max, num):
            candidates[j] = False
    return candidates


def print_grid(gird, index_is_prime):
    # Using the colored function to return a colored string
    #text = colored("Hello", "green", attrs=["bold"])
    #text += colored("World!", "red", attrs=["bold"])
    #print(text)
    biggest = len(grid)*len(grid)
    biggest_str = str(biggest)
    print_width = len(biggest_str) + 1
    for j in range(len(grid)):
        row = colored("", "grey", attrs=[])
        for i in range(len(grid)):
            vi = grid[i][j]
            prime = index_is_prime[vi-1]
            v = str(vi).center(print_width)
            colord_v = colored(v, "black", "on_black")
            if prime:
                colord_v = colored(v, "green", "on_red", attrs=["bold"])
            row += colord_v
        print(row)
    

def populate_grid(gird):
    i = len(grid) - 1
    j = len(grid) - 1
    side = len(grid)
    v = len(grid)*len(grid)
    dir = "l"
    steps = side - 1
    ring_steps = steps
    while v > 0:
        grid[i][j] = v
        v -=1
        if dir == "l":
            if steps > 0:
                i -= 1
                steps -=1
            else:
                dir = "u"
                steps = ring_steps
        if dir == "u":
            if steps > 0:
                j -= 1
                steps -=1
            else:
                dir = "r"
                steps = ring_steps
        if dir == "r":
            if steps > 0:
                i += 1
                steps -=1
            else:
                dir = "d"
                steps = ring_steps
        if dir == "d":
            if steps > 1:
                j += 1
                steps -=1
            else:
                dir = "l"
                ring_steps -= 2
                steps = ring_steps
                i -= 1
size = 41
biggest = size * size
grid = get_grid(size)
populate_grid(grid)
index_is_prime = sieve_of_eratosthenes(biggest)
print_grid(grid, index_is_prime)


