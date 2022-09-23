""""
    Module lab1 - used to building an expert base and knowledge
      Functions:
        generate_simple_rules - function that generates simple rules for check
        generate_stairway_rules - function that generates stairway rules for check
        generate_ring_rules - function that generates ring rules for check
        generate_random_rules - function that generates random rules for check
        generate_seq_facts - function that generates seq facts
        generate_rand_facts - function that generates random facts
        set_rang - function that establishes facts
        max_rangs - function that calculates max rang of rule
        sort_rangs - function that sorts list of rules by rang of rule
        check_rules - function that checks rules conflicts
        check_rules_vs_facts - function that checks facts
        main - main function
"""
from random import choice, shuffle, randint
from time import time


def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    """ Function generate simple rules
                Args :
                        code_max - max value
                        n_max - max number of elements in condition
                        log_oper_choice - operation in rule
                Returns :
                        rules - generating rules
    """
    rules = []
    for j in range(0, n_generate):
        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': code_max + j
        }
        rules.append(rule)
    shuffle(rules)
    return rules


def generate_stairway_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    """ Function generate stairway rules
                Args :
                        code_max - max value
                        n_max - max number of elements
                        n_generate - generate number of elements
                        log_oper_choice - operation in rule
                Returns :
                        rules - generating rules
    """
    rules = []
    for j in range(0, n_generate):
        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(i + j)
        rule = {
            'if': {
                log_oper: items
            },
            'then': i + j + 1
        }
        rules.append(rule)
    shuffle(rules)
    return rules


def generate_ring_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    """ Function generate ring rules
                Args :
                        code_max - max value
                        n_max - max number of elements
                        n_generate - generate number of elements
                        log_oper_choice - operation in rule
                Returns :
                        rules - generating rules
    """
    rules = generate_stairway_rules(code_max, n_max, n_generate - 1, log_oper_choice)
    log_oper = choice(log_oper_choice)  # not means and-not (neither)
    if n_max < 2:
        n_max = 2
    n_items = randint(2, n_max)
    items = []
    for i in range(0, n_items):
        items.append(code_max - i)
    rule = {
        'if': {
            log_oper: items
        },
        'then': 0
    }
    rules.append(rule)
    shuffle(rules)
    return rules


def generate_random_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    """ Function generate random rules
                Args :
                        code_max - max value
                        n_max - max number of elements
                        n_generate - generate number of elements
                        og_oper_choice - operation in rule
                Returns :
                       rules - generating rules
    """
    rules = []
    for j in range(0, n_generate):
        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': randint(1, code_max)
        }
        rules.append(rule)
    shuffle(rules)
    return rules


def generate_seq_facts(number_facts):
    """ Function generate seq facts
                Args :
                        number_facts - numbers of facts
                Returns :
                        facts - generating facts
    """
    facts = list(range(0, number_facts))
    shuffle(facts)
    return facts


def generate_rand_facts(code_max, number_facts):
    """ Function generate random facts
                Args :
                        code_max - max value of fact
                        number_facts - numbers of facts
                Returns :
                        facts - generating facts
    """
    facts = []
    for i in range(0, number_facts):
        facts.append(randint(0, code_max))
    return facts


# not final version
def set_rang(rules):  # set rangs for rules
    """ Function set rangs for rules
                Args :
                        rules - our rules for which set rangs
                Returns :
                        correct_rules - rules which have rang
    """
    rangs = [-1] * 2 * len(rules)
    then_rules = list()
    max_rang = 0
    for rule in rules:
        if rule['then']:
            then_rules.append(rule['then'])
    for rule in rules:
        for keys in rule['if']:
            for item in rule['if'][keys]:
                if item in then_rules:
                    rangs[item] = max_rang + 1
                    if rangs[item] > max_rang:
                        max_rang = rangs[item]
                else:
                    rangs[item] = 0
                    if rangs[item] > max_rang:
                        max_rang = rangs[item]
            rangs[rule['then']] = max_rang + 1
            max_rang = 0
    del then_rules
    correct_rangs = list()
    for item in rangs:
        if item != -1:
            correct_rangs.append(item)
    return correct_rangs


def max_rangs(rule, rangs):  # calculate max rang of rule
    """ Function determine max rang of rule
                Args :
                        rule - our rules to determine max rang
                        rangs - list rangs of rules
                Returns :
                        max_rang - max rang of rule
    """
    max_rang_if = 0
    for keys in rule['if']:
        for value in rule['if'][keys]:
            if rangs[value] > max_rang_if:
                max_rang_if = rangs[value]
    if rangs[rule['then']]:
        if max_rang_if > rangs[rule['then']]:
            max_rang = max_rang_if
        else:
            max_rang = rangs[rule['then']]
    else:
        max_rang = max_rang_if
    return max_rang


def sort_rangs(rules, rangs):  # sort rules by rang
    """ Function sort rules by rangs
                Args :
                        rules - our rules
                        rangs - list rangs of rules
    """
    for i in range(len(rules) - 1):
        for j in range(len(rules) - i - 1):
            if max_rangs(rules[j], rangs) > max_rangs(rules[j+1], rangs):
                rangs[j] = rangs[j+1]
                temp_rang = rangs[j]
                rangs[j+1] = temp_rang
                rules[j] = rules[j+1]
                temp_rule = rules[j]
                rules[j+1] = temp_rule


def check_rules(rules):
    """ Function check rules conflicts
                Args :
                        rules - our rules
                Returns :
                        correct_rules - rules without conflicts
    """
    start_check = time()
    if_rules = list()
    then_rules = list()
    correct_rules = list()
    #rangs = set_rang(rules)
    #sort_rangs(rules, rangs)
    for rule in rules:
        if rule['if']:
            if_rules.append(rule['if'])
        if rule['then']:
            then_rules.append(rule['then'])
    for i in range(len(rules) - 1):
        for j in range(i + 1, len(rules)-1):
            if i >= j:
                return 0
            if then_rules[i] == then_rules[j]:  # check "if and/or A then B -> if not A then B"
                if ('and' in rules[i].keys() and 'not' in rules[j].keys) or ('and' in rules[j].keys() and 'not' in rules[i].keys):
                    if if_rules[j]['and'] == if_rules[i]['not'] or if_rules[i]['and'] == if_rules[j]['not']:
                        rules[j].clear()
                        rules[i].clear()
                        print(i, ' disagree ', j)
                if ('or' in rules[j].keys() and 'not' in rules[i].keys) or ('or' in rules[i].keys() and 'not' in rules[j].keys):
                    if if_rules[j]['or'] == if_rules[i]['not'] or if_rules[i]['or'] == if_rules[j]['not']:
                        rules[j].clear()
                        rules[i].clear()
                        print(i, ' disagree ', j)
            if 'not' in if_rules[i].keys() and 'not' in if_rules[j].keys(): # check "if not A then B -> if not B then A"
                if then_rules[i] in if_rules[j]['not'] and then_rules[j] in if_rules[i]['not']:
                    rules[i].clear()
                    rules[j].clear()
                    print(i, ' disagree ', j)  # check "if not A then B -> if not C then A"
                if then_rules[i] in if_rules[j]['not'] and then_rules[j] not in if_rules[i]['not']:
                    rules[i].clear()
                    rules[j].clear()
                    print(i, ' disagree ', j)
    for rule in rules:
        if rule != {}:
            correct_rules.append(rule)
    end_check = time()
    time_result = end_check - start_check
    print('\ntime to check conflicts ', time_result)
    return correct_rules


def check_rules_vs_facts(rules, facts):
    """ Function check rules conflicts
                Args :
                        rules - our rules
                        facts - our generating facts
    """
    start_check = time()
    result = list()
    temp = 0
    size = 0
    for rule in rules:
        if rule != {}:
            for key in rule['if']:
                if key == 'and':
                    for item in rule['if'][key]:
                        size = len(rule['if'][key])
                        if item in facts:
                            temp += 1
                    if temp == size:
                        result.append(rule['then'])
                        temp = 0
                    else:
                        result.append(0)
                        temp = 0
                if key == 'or':
                    for item in rule['if'][key]:
                        if item in facts:
                            result.append(rule['then'])
                            break
                if key == 'not':
                    for item in rule['if'][key]:
                        size = len(rule['if'][key])
                        if item not in facts:
                            temp += 1
                    if temp == size:
                        result.append(rule['then'])
                        temp = 0
                    else:
                        result.append(0)
                        temp = 0
    print(result)
    end_check = time()
    time_result = end_check - start_check
    print('\ntime to check facts vs rules ', time_result)


def main():
    """
        main function for work
    """
    # generate rules
    time_start = time()
    number_rules = 10000
    number_facts = 1000
    rules = generate_simple_rules(100, 4, number_rules)
    random_rules = generate_random_rules(100, 4, number_rules)
    stairway_rules = generate_stairway_rules(100, 4, number_rules)
    ring_rules = generate_ring_rules(100, 4, number_rules)

    # generate facts
    facts = generate_rand_facts(100, number_facts)
    print("%d rules for each type generated in %f seconds" % (number_rules, time() - time_start))

    # merge rules
    all_rules = list()
    for rule in rules:
        all_rules.append(rule)
    for rule in stairway_rules:
        all_rules.append(rule)
    for rule in random_rules:
        all_rules.append(rule)
    for rule in ring_rules:
        all_rules.append(rule)

    # load and validate rules
    # check rules
    correct_rules = check_rules(all_rules)

    # check facts vs rules
    time_start = time()
    check_rules_vs_facts(correct_rules, facts)

    print("%d facts validated vs %d rules in %f seconds" % (number_facts, 4*number_rules, time() - time_start))


if __name__ == '__main__':
    main()
