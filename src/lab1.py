from random import choice, shuffle, randint
from time import time
import matplotlib.pyplot as plt


def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
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
    return (rules)


def generate_stairway_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
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
    return (rules)


def generate_ring_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
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
    return (rules)


def generate_random_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
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
    return (rules)


def generate_seq_facts(M):
    facts = list(range(0, M))
    shuffle(facts)
    return facts


def generate_rand_facts(code_max, M):
    facts = []
    for i in range(0, M):
        facts.append(randint(0, code_max))
    return facts


# not final version
def set_rang(rules):
    rangs = [None] * len(rules)
    temp = [None] * len(rules)
    then_rules = list()
    max_rang = 0
    for rule in rules:
        for keys in rule['if']:
            for item in rule['if'][keys]:
                if temp[item] is None:
                    if temp[item] in then_rules:
                        rangs[item] = max_rang + 1
                        temp[item] = 0
                        if rangs[item] > max_rang:
                            max_rang = rangs[item]
                    else:
                        rangs[item] = 0
                        temp[item] = 0
                        if rangs[item] > max_rang:
                            max_rang = rangs[item]
                if temp[rule['then']] is None:
                    rangs[rule['then']] = max_rang + 1
                    temp[rule['then']] = 0
                    if rangs[item] > max_rang:
                        max_rang = rangs[item]
        #max_rang = 0
    del temp
    del then_rules
    return rangs


def check_rules(rules):
    start_check = time()
    if_rules = list()
    then_rules = list()
    size = len(rules)
    right_rules = list()
    for rule in rules:
        if rule['if']:
            if_rules.append(rule['if'])
        if rule['then']:
            then_rules.append(rule['then'])
    for i in if_rules:
        sorted(i.values())
    for i in range(size - 1):
        for j in range(i + 1, size):
            try:
                if if_rules[i] == if_rules[j] and then_rules[i] != then_rules[j]: # check "if A then B -> if A then C"
                    rules[i].clear()
                    rules[j].clear()
                    print(i, ' disagree ', j)
                if then_rules[i] == then_rules[j]:  # check "if and/or A then B -> if not A then B"
                    if ('and' in rules[i].keys() and 'not' in rules[j].keys) or ('and' in rules[j].keys() and 'not' in rules[i].keys):
                        if if_rules[i]['and'] == if_rules[j]['not'] or if_rules[j]['and'] == if_rules[i]['not']:
                            rules[i].clear()
                            rules[j].clear()
                            print(i, ' another disagree ', j)
                    if ('or' in rules[i].keys() and 'not' in rules[j].keys) or ('or' in rules[j].keys() and 'not' in rules[i].keys):
                        if if_rules[i]['or'] == if_rules[j]['not'] or if_rules[j]['or'] == if_rules[i]['not']:
                            rules[i].clear()
                            rules[j].clear()
                            print(i, ' another disagree ', j)
            except IndexError:
                continue
    for rule in rules:
        if rule != {}:
            right_rules.append(rule)
    end_check = time()
    time_result = end_check - start_check
    print('\ntime to check conflicts ', time_result)
    plt.plot([0, time_result], [1000, len(rules)], 'o-g', alpha=0.7, label="first", lw=5, mec='g', mew=4, ms=5)
    plt.show()
    return right_rules


def check_rules_vs_facts(rules, facts):
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
    plt.plot([0, time_result], [1000, len(rules)], 'o-b', alpha=0.7, label="first", lw=5, mec='b', mew=4, ms=5)
    plt.show()


def main():
    # samples:
    # print(generate_simple_rules(100, 4, 10))
    # print(generate_random_rules(100, 4, 10))
    # print(generate_stairway_rules(100, 4, 10, ["or"]))
    # print(generate_ring_rules(100, 4, 10, ["or"]))

    # generate rules
    time_start = time()
    N = 10000
    M = 1000
    rules = generate_simple_rules(100, 4, N)
    random_rules = generate_random_rules(100, 4, N)
    stairway_rules = generate_stairway_rules(100, 4, N)
    ring_rules = generate_ring_rules(100, 4, N)

    # merge rules
    all_rules = list()
    for item in rules:
        all_rules.append(item)
    for item in stairway_rules:
        all_rules.append(item)
    for item in random_rules:
        all_rules.append(item)
    for item in ring_rules:
        all_rules.append(item)

    set_rang(all_rules)
    #
    # generate facts
    facts = generate_rand_facts(100, M)
    print("%d rules generated in %f seconds" % (N, time() - time_start))

    # load and validate rules
    # check rules
    right_rules = check_rules(all_rules)

    # check facts vs rules
    time_start = time()
    check_rules_vs_facts(right_rules, facts)
    print("%d facts validated vs %d rules in %f seconds" % (M, N, time() - time_start))


if __name__ == '__main__':
    main()
