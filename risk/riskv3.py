# simulate a list of risk battles
import random

sim_num = 100000
# sim_num = 3
print_offset = sim_num / 100


class scenario:
    def __init__(self, name, atk_num, def_num):
        self.name = name
        self.attack_num = atk_num
        self.defence_num = def_num
        self.defender_win = 0
        self.attacker_win = 0

    def print_result(self):
        print("results for ", self.name)
        print("there were", sim_num, "battles")
        print(
            "attackers won",
            self.attacker_win,
            self.attacker_win / sim_num,
            "of the battles",
        )
        print(
            "defenders won",
            self.defender_win,
            self.defender_win / sim_num,
            "of the battles",
        )


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


# runs a given scenario sim_num times and saves the result to the scenario
def run_scenario(scenario):
    scenario.attacker_win = 0
    scenario.defender_win = 0
    for i in range(sim_num):
        if (i + 1) % print_offset == 0:
            print(scenario.name, "progress", i / sim_num)
        attack_num_sim = scenario.attack_num
        defence_num_sim = scenario.defence_num
        while attack_num_sim > 0 and defence_num_sim > 0:
            attack_dice = roll_dice(min(attack_num_sim, 3))
            attack_dice.sort(reverse=True)
            defence_dice = roll_dice(min(defence_num_sim, 2))
            defence_dice.sort(reverse=True)
            attackers_killed, defenders_killed = decide_death(attack_dice, defence_dice)
            attack_num_sim -= attackers_killed
            defence_num_sim -= defenders_killed

        if attack_num_sim <= 0:
            scenario.defender_win = scenario.defender_win + 1
        else:
            scenario.attacker_win = scenario.attacker_win + 1


scenario_list = [
    scenario("10v10", 10, 10),
    scenario("20v25", 20, 25),
    scenario("very big", 1000, 1003),
]

for s in scenario_list:
    run_scenario(s)
    s.print_result()
