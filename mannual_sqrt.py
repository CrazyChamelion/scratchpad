import math
import sys

def manual_sqrt(val):
    current = val
    i = 0
    while True:
        new = 0.5*(current + val/current)
        dif = abs(new - current)
        current = new
        i = i + 1
        if dif < 0.01:
            break
    return (i, current)

def pretty_print(val):
    iter, result = manual_sqrt(val)
    error = abs(math.sqrt(val) - result)
    print(f"sqrt({val}) ~ {result}, err = {error}, took {iter} tries")
"""
pretty_print(4)
pretty_print(16)
pretty_print(25)
pretty_print(100)
pretty_print(127.35)
pretty_print(9876543210)
pretty_print(9876543210.923)
pretty_print(7.21 * 10**3)
pretty_print(55125)
pretty_print(55125*55125)
pretty_print(2)
"""

def stupid_sqrt(x):
    guess=0.5
    iter = 1
    margin = 1
    while True:
        sqr = guess*guess
        if sqr < x+margin and sqr > x-margin or sqr == x: 
            return iter, guess
        if sqr > x:
            print ("SHIT SHIT SHIT SHIT SHIT")
            sys.exit()
        guess=guess+0.0005
        iter += 1

def pretty_print_stupid(val):
    iter, result = stupid_sqrt(val)
    error = abs(math.sqrt(val) - result)
    print(f"sqrt({val}) ~ {result}, err = {error}, took {iter} tries")

def compare_good_to_bad(val):
    good_itter, good = manual_sqrt(val)
    bad_itter, bad = stupid_sqrt(val)

    delta_iter = bad_itter - good_itter
    error = abs(good - bad)

    print(f"sqrt({val}) stupid took {delta_iter} more iterations to produce an error of {error}. Stupid result = {bad}")

#compare_good_to_bad(10)
#compare_good_to_bad(25)
#compare_good_to_bad(100)
#compare_good_to_bad(2500)
compare_good_to_bad(36377527)