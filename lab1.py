from random import choice, shuffle, randint
from time import time


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


def check_rules(rules):
    start_check = time()
    if_rules = list()
    then_rules = list()
    for rule in rules:
        if rule['if']:
            if_rules.append(rule['if'])
        if rule['then']:
            then_rules.append(rule['then'])
    size = len(rules)
    for i in range(size-1):
        for j in range(i+1, size):
            if if_rules[i] == if_rules[j]:
                if then_rules[i] != then_rules[j]:
                    print(i, ' disagree ', j)
    end_check = time()
    time_result = end_check - start_check
    print('\ntime to check conflicts ',time_result)


def check_rules_vs_facts(rules, facts):
    start_check = time()
    result = list()
    temp = 0
    size = 0
    for rule in rules:
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


# samples:
print(generate_simple_rules(100, 4, 10))
print(generate_random_rules(100, 4, 10))
print(generate_stairway_rules(100, 4, 10, ["or"]))
print(generate_ring_rules(100, 4, 10, ["or"]))

# generate rules and facts and check time
time_start = time()
N = 10000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
print("%d rules generated in %f seconds" % (N, time() - time_start))
# load and validate rules
# YOUR CODE HERE
check_rules(rules)
# check facts vs rules
time_start = time()

# YOUR CODE HERE
check_rules_vs_facts(rules, facts)
print("%d facts validated vs %d rules in %f seconds" % (M, N, time() - time_start))
