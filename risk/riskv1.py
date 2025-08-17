# simulate the first dice comparison of a risk battle
import random 
sim_num = 100000
attack_num = 3
defence_num = 2
defender_win = 0 
attacker_win = 0

for i in range (1,sim_num+1):
    highest_attack = 0
    highest_defence = 0     
    
    for b in range (1, attack_num+1):
        attack_dice =  random.randint (1,6) 
        if attack_dice >= highest_attack:
            highest_attack = attack_dice 
    for b in range (1, defence_num+1):
        defence_dice =  random.randint (1,6) 
        if defence_dice >= highest_defence:
            highest_defence = defence_dice 
    
    if highest_defence >= highest_attack:
        defender_win = defender_win +1
    else:
        attacker_win = attacker_win + 1
print ("there were" , sim_num , "battles")
print ("attackers won" , attacker_win, attacker_win / sim_num, "of the battles")
print ("defenders won" , defender_win, defender_win / sim_num, "of the battles")