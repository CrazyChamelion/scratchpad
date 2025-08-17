# simulate a risk battle with vatriable number of attackers and defenders
import random

sim_num = 100000
#sim_num = 3
attack_num = 20
defence_num = 25
defender_win = 0 
attacker_win = 0

# rolls a number of d6 and returns a list
def roll_dice(n):
    result = []
    for i in range(n):
        result.append(random.randint(1, 6))
    return result

# given dice for attacker and defenders return number of attacker killed, number of defenders killed
def decide_death(attack_dice, defence_dice):
    battles = min(len(attack_dice), len(defence_dice))
    attackers_killed = 0
    defenders_killed = 0
    for b in range(battles):
        if defence_dice[b] >= attack_dice[b]:
            attackers_killed += 1
        else:
            defenders_killed += 1
    return attackers_killed, defenders_killed

for i in range (sim_num):
    attack_num_sim = attack_num
    defence_num_sim = defence_num
    while attack_num_sim > 0 and defence_num_sim > 0:
        attack_dice = roll_dice(min(attack_num_sim, 3))
        attack_dice.sort(reverse=True)
        defence_dice = roll_dice(min(defence_num_sim, 2))
        defence_dice.sort(reverse=True)
        #print("attackers", attack_num_sim, "defenders", defence_num_sim)
        #print("atk roll", attack_dice, "def roll", defence_dice)
        attackers_killed, defenders_killed = decide_death(attack_dice, defence_dice)
        #print("atk killed", attackers_killed, "def killed", defenders_killed)
        attack_num_sim -= attackers_killed
        defence_num_sim -= defenders_killed
    
    #print("final atk", attack_num_sim, "final def", defence_num_sim)
    if attack_num_sim <=0:
        defender_win = defender_win +1
    else:
        attacker_win = attacker_win + 1
    #print(80*'-')
print ("there were" , sim_num , "battles")
print ("attackers won" , attacker_win, attacker_win / sim_num, "of the battles")
print ("defenders won" , defender_win, defender_win / sim_num, "of the battles")