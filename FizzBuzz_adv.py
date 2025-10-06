""" REQUIRMENTS
1 Dynamic divisibility rules eg one time /3 = fiz another time /5 = fiz 
2 pattern dettion, after 3 fizz say mega fizz, after 3 buzz say mega buzz, ect
3 Grid formating
4 #opptional, prime detection
"""

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

def convert_candidates(candidates):
    result = []
    for i in range(len(candidates)):
        if candidates[i]:
            result.append(i+1)
    return result

class rule:
    def __init__(self, phrase):
        self.phrase = phrase

    def rule_applies(self, num):
        pass

class divisor_rule(rule):
    def __init__(self, phrase, div):
        super().__init__(phrase)
        self.div = div
    
    def rule_applies(self, num):
        return num % self.div == 0
    
class prime_rule(rule):
    def __init__(self, phrase, all_primes):
        super().__init__(phrase)
        self.all_primes = all_primes
    
    def rule_applies(self, num):
        return num in self.all_primes

def fiz_buz_by_rules(rules, max, mega_count):
    results = []
    rule_count = [0]*len(rules)
    for i in range(1, max):
        phrase = ""
        for j in range(len(rules)):
            r = rules[j]
            if r.rule_applies(i):
                rule_count[j] += 1
                if rule_count[j] == mega_count:
                    phrase += "MEGA-"
                    rule_count[j] = 0
                phrase += r.phrase + "-"
        if len(phrase) > 0:
            if phrase[len(phrase)-1] == "-":
                phrase = phrase[0:len(phrase)-1]
            results.append((i, phrase))
    return results

def print_in_columns(stuff, col):
    i = 0
    while i < len(stuff):
        this_col = ""
        for j in range(col):
            item = f"{stuff[i][0]} {stuff[i][1]}"
            this_col += f"{item:<25}"
            i += 1
        print(this_col)

MAX = 100

primes = convert_candidates(sieve_of_eratosthenes(MAX))
print(f"primes beween 1 and {MAX} are {primes}")

rules = []
rules.append(divisor_rule("fiz", 3))
rules.append(divisor_rule("buz", 5))
rules.append(prime_rule("prim", primes))

result = fiz_buz_by_rules(rules, MAX, 4)
print_in_columns(result, 3)
