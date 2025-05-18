import random
import time

from helpers import total_cost, delta_2opt, delta_vertex


def local_steepest_vertices(cycle1, cycle2, distance_matrix):
    start_time = time.time()
    c1 = cycle1[:]
    c2 = cycle2[:]

    while True:
        best_delta = 0.0
        best_move = None

        n1 = len(c1)
        for i in range(n1):
            for j in range(i+1, n1):
                delta = delta_vertex(c1, i, j, distance_matrix)

                if delta < best_delta:
                    best_delta = delta
                    best_move = (1, i, j)

        n2 = len(c2)

        for i in range(n2):
            for j in range(i+1, n2):
                delta = delta_vertex(c2, i, j, distance_matrix)

                if delta < best_delta:
                    best_delta = delta
                    best_move = (2, i, j)

        if best_move is None or best_delta >= 0:
            break

        which_cycle, i, j = best_move

        if which_cycle == 1:
            c1[i], c1[j] = c1[j], c1[i]
        else:
            c2[i], c2[j] = c2[j], c2[i]

    return c1, c2, (time.time() - start_time)


def local_steepest_edges(cycle1, cycle2, distance_matrix):
    start_time = time.time()
    c1 = cycle1[:]
    c2 = cycle2[:]

    while True:
        best_delta = 0.0
        best_move = None

        n1 = len(c1)
        for i in range(n1):
            for j in range(i+2, n1):
                delta = delta_2opt(c1, i, j, distance_matrix)

                if delta < best_delta:
                    best_delta = delta
                    best_move = (1, i, j)

        n2 = len(c2)

        for i in range(n2):
            for j in range(i+2, n2):
                delta = delta_2opt(c2, i, j, distance_matrix)

                if delta < best_delta:
                    best_delta = delta
                    best_move = (2, i, j)

        if best_move is None or best_delta >= 0:
            break

        which_cycle, i, j = best_move

        if which_cycle == 1:
            c1 = c1[:i+1] + list(reversed(c1[i+1:j+1])) + c1[j+1:]
        else:
            c2 = c2[:i+1] + list(reversed(c2[i+1:j+1])) + c2[j+1:]

    return c1, c2, (time.time() - start_time)

def local_greedy_vertices(cycle1, cycle2, distance_matrix):
    start_time = time.time()
    c1 = cycle1[:]
    c2 = cycle2[:]

    while True:
        improved = False
        pairs = []

        n1 = len(c1)
        for i in range(n1):
            for j in range(i+1, n1):
                pairs.append((1, i, j))

        n2 = len(c2)
        for i in range(n2):
            for j in range(i+1, n2):
                pairs.append((2, i, j))

        random.shuffle(pairs)

        for (which_cycle, i, j) in pairs:
            if which_cycle == 1:
                delta = delta_vertex(c1, i, j, distance_matrix)

                if delta < 0:
                    c1[i], c1[j] = c1[j], c1[i]
                    improved = True
                    break
            else:
                delta = delta_vertex(c2, i, j, distance_matrix)

                if delta < 0:
                    c2[i], c2[j] = c2[j], c2[i]
                    improved = True
                    break

        if not improved:
            break

    return c1, c2, (time.time() - start_time)

def local_greedy_edges(cycle1, cycle2, distance_matrix):
    start_time = time.time()
    c1 = cycle1[:]
    c2 = cycle2[:]

    while True:
        improved = False
        pairs = []

        n1 = len(c1)
        for i in range(n1):
            for j in range(i+2, n1):
                pairs.append((1, i, j))

        n2 = len(c2)
        for i in range(n2):
            for j in range(i+2, n2):
                pairs.append((2, i, j))

        random.shuffle(pairs)
        for (which_cycle, i, j) in pairs:
            if which_cycle == 1:
                delta = delta_2opt(c1, i, j, distance_matrix)
                if delta < 0:
                    c1 = c1[:i+1] + list(reversed(c1[i+1:j+1])) + c1[j+1:]
                    improved = True
                    break
            else:
                delta = delta_2opt(c2, i, j, distance_matrix)
                if delta < 0:
                    c2 = c2[:i+1] + list(reversed(c2[i+1:j+1])) + c2[j+1:]
                    improved = True
                    break

        if not improved:
            break

    return c1, c2, (time.time() - start_time)

def random_walk(cycle1, cycle2, distance_matrix, time_limit=1.0):
    start_time = time.time()
    c1 = cycle1[:]
    c2 = cycle2[:]
    best_c1 = c1[:]
    best_c2 = c2[:]
    best_cost = total_cost(c1, c2, distance_matrix)

    while time.time() - start_time < time_limit:
        move_type = random.choice(["swap_in_cycle1", "swap_in_cycle2", "swap_between_cycles"])

        if move_type == "swap_in_cycle1" and len(c1) > 1:
            i, j = random.sample(range(len(c1)), 2)
            c1[i], c1[j] = c1[j], c1[i]

        elif move_type == "swap_in_cycle2" and len(c2) > 1:
            i, j = random.sample(range(len(c2)), 2)
            c2[i], c2[j] = c2[j], c2[i]

        elif move_type == "swap_between_cycles" and len(c1) > 0 and len(c2) > 0:
            i = random.randrange(len(c1))
            j = random.randrange(len(c2))
            c1[i], c2[j] = c2[j], c1[i]

        cur_cost = total_cost(c1, c2, distance_matrix)

        if cur_cost < best_cost:
            best_cost = cur_cost
            best_c1 = c1[:]
            best_c2 = c2[:]

    return best_c1, best_c2
