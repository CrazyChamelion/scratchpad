import random 
gear = ["shield" ,"helmet", "breastplate","wand","staff","necklace","bracelet","gem","sword","spear","gun","gem","crossbow","hand grenade","spear","panties","underwear", "steal toed boots","fork",]
beforeenchant = ["+1","flaming", "self harming", "+2","+3","acidid", "one time use", "demoic", "very shiney", "rusty", "explosive" ]
afterenchant = ["of haste", "of ogerslaying", " of self immolation","of polymporph", "of serpantkind" , "of the gods"]
name = ["bill", "reggy" , "susan" , "kevin", "noah" , "kim" , "Jannet" , "strahd" , "Jill", ]
aftername = ["the short" , "the pimp" , "the tall" , "the fat" , "the unjust" , "the mildly ok", "the not so heroic", "the cursed" , "the afriad"]

for i in range(20):
    randomgear = random.choice(gear)
    random_b_enchant = random.choice(beforeenchant)
    random_a_enchant= random.choice(afterenchant)
    randomname = random.choice(name)
    random_a_name = random.choice(aftername)
    print (f"{randomname} {random_a_name} has a {random_b_enchant} {randomgear} {random_a_enchant}")