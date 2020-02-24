import random
from operator import itemgetter


def fitness(indi):
    total = 0
    total = sum(indi["gen"])
    return total


def individual(nb_feature, total_feature):
    a = [i for i in range(total_feature)]
    random.shuffle(a)
    indi = {"gen": a[:nb_feature], "fitness": 0.0}
    indi["fitness"] = fitness(indi)
    return indi


def selection(popu, population_size):
    new_list = sorted(popu, key=itemgetter("fitness"), reverse=False)
    return new_list[:population_size]


def crossover(father, mother, total_feature):
    # print(father, mother)
    f_child = {"gen": [], "fitness": 0.0}
    m_child = {"gen": [], "fitness": 0.0}
    n = len(father["gen"])
    cut_a = random.randint(1, n - 1)
    cut_b = random.randint(1, n - 1)
    while cut_b == cut_a:
        cut_b = random.randint(1, n - 1)
    start = min(cut_a, cut_b)
    end = max(cut_a, cut_b)
    # print start, end
    f_temp = father["gen"][start:end]
    m_temp = mother["gen"][start:end]
    # print temp
    mask = [i for i in range(total_feature)]
    random.shuffle(mask)
    #  calculate f_child
    index = 0
    while index < start:
        for item in mother["gen"]:
            if item not in f_temp and item not in f_child["gen"]:
                f_child["gen"].append(item)
                index = index + 1
                break
    f_child["gen"].extend(f_temp)
    index = len(f_child["gen"])
    while index < n:
        for item in mother["gen"]:
            if item not in f_child["gen"]:
                f_child["gen"].append(item)
                index = index + 1
                break
    index = len(f_child["gen"])
    while index < n:
        for item in mask:
            if item not in f_child["gen"]:
                f_child["gen"].append(item)
                index = index + 1
                break
    f_child["fitness"] = fitness(f_child)
    #  calculate m_child
    index = 0
    while index < start:
        for item in father["gen"]:
            if item not in m_temp and item not in m_child["gen"]:
                m_child["gen"].append(item)
                index = index + 1
                break
    m_child["gen"].extend(m_temp)
    index = len(m_child["gen"])
    while index < n:
        for item in father["gen"]:
            if item not in m_child["gen"]:
                m_child["gen"].append(item)
                index = index + 1
                break
    index = len(m_child["gen"])
    while index < n:
        for item in mask:
            if item not in m_child["gen"]:
                m_child["gen"].append(item)
                index = index + 1
                break
    m_child["fitness"] = fitness(m_child)
    # print "temp1 =", gen1, "temp2 =", gen2, "Off =", off
    return f_child, m_child


def mutation(father, total_feature):
    mask = [i for i in range(total_feature)]
    random.shuffle(mask)
    off = {"gen": [], "fitness": 0.0}
    n = len(father["gen"])
    j = random.randint(1, n-1)
    off["gen"] = father["gen"][:j]
    for item in mask:
        if item not in father["gen"]:
            off["gen"].append(item)
            break
    off["gen"].extend(father["gen"][j+1:])
    off["fitness"] = fitness(off)
    return off


def evolution(nb_feature, total_feature, population_size, pc=0.8, pm=0.2, max_gen=1000):
    population = []
    for _ in range(population_size):
        population.append(individual(nb_feature=nb_feature, total_feature=total_feature))
    t = 0
    while t < max_gen:
        for i, _ in enumerate(population):
            r = random.random()
            if r < pc:
                j = random.randint(0, population_size-1)
                while j == i:
                    j = random.randint(0, population_size - 1)
                f_child, m_child = crossover(population[i], population[j], total_feature=total_feature)
                population.append(f_child)
                population.append(m_child)
            if r < pm:
                off = mutation(population[i], total_feature=total_feature)
                population.append(off)
        population = selection(population, population_size)
        print("t =", t, "fitness =", population[0])
        t = t + 1
    return population[0]
