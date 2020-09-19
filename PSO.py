import random
from operator import itemgetter
import copy
import math
import numpy as np


w = 1
c1 = 1
c2 = 1


def fitness(arr):
    return sum(arr)


def individual(total_feature):
    location = np.random.rand(total_feature)
    velocity = np.zeros(total_feature)
    fit = fitness(np.rint(location))
    return {"location": location, "velocity": velocity, "fitness": fit, "pbest": location, "fit_best": fit}


def population(pop_size, total_feature):
    pop = []
    for _ in range(pop_size):
        pop.append(individual(total_feature=total_feature))
    return pop


def multi(arr1, arr2):
    return arr1 * arr2


def add(arr1, arr2):
    return arr1 + arr2 - arr1 * arr2


def minus(arr):
    a = np.random.randint(1, size=len(arr)) + 1
    return a - arr


def gbest(popu):
    id_min = min(range(len(popu)), key=lambda index: popu[index]['fitness'])
    return popu[id_min]["location"]


def repair(arr):
    if np.max(arr) == np.min(arr):
        if arr[0] > 1:
            return np.ones(len(arr))
        elif arr[0] < 0:
            return np.zeros(len(arr))
        else:
            return arr
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))


def evolution(pop_size, total_feature, max_time):
    pop = population(pop_size=pop_size, total_feature=total_feature)
    t = 0
    while t <= max_time:
        t = t + 1
        g = gbest(popu=pop)
        # print(t, fitness(np.rint(g)), np.rint(g),)
        # for indi in pop:
        #     print(indi["fitness"],)
        # print()
        for i, _ in enumerate(pop):
            r1 = np.random.rand(total_feature)
            r2 = np.random.rand(total_feature)
            loc = c1 * r1 * (pop[i]["pbest"] - pop[i]["location"])
            glo = c2 * r2 * (g - pop[i]["location"])
            pop[i]["velocity"] = w * pop[i]["velocity"] + loc + glo
            # pop[i]["velocity"] = repair(pop[i]["velocity"])
            pop[i]["location"] = pop[i]["location"] + pop[i]["velocity"]
            pop[i]["location"] = repair(pop[i]["location"])
            pop[i]["fitness"] = fitness(np.rint(pop[i]["location"]))
            if pop[i]["fitness"] < pop[i]["fit_best"]:
                pop[i]["pbest"] = pop[i]["location"]
                pop[i]["fit_best"] = pop[i]["fitness"]
    g = gbest(popu=pop)
    return np.rint(g), fitness(np.rint(g))
