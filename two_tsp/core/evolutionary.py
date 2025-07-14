import random

from two_tsp.core.construct import construct_random, insertion_weighted_regret
from two_tsp.core.helpers import cycles_cost
from two_tsp.core.local_search_optimized import local_search_with_move_list


def recombine(parents):
    parent1, parent2 = parents[0][0], parents[1][0]

    edges_removed_pos1 = []
    removed_vertices = []
    for c in range(2):
        cycle1 = parent1[c]
        n = len(cycle1)

        for i in range(n):
            v = cycle1[i]
            v_next = cycle1[(i + 1) % n]

            edge_exists = False

            for c2 in range(2):
                cycle2 = parent2[c2]
                m = len(cycle2)

                for j in range(m):
                    u = cycle2[j]
                    u_next = cycle2[(j + 1) % m]

                    if (v == u and v_next == u_next) or (v == u_next and v_next == u):
                        edge_exists = True
                        break

                if edge_exists:
                    break

            if not edge_exists:
                edges_removed_pos1.append((c, i))

    child = [list(parent1[0]), list(parent1[1])]

    edges_removed = [set() for _ in range(2)]
    for c, i in edges_removed_pos1:
        n = len(child[c])
        edges_removed[c].update({i, (i + 1) % n})

    for c in range(2):
        cycle = child[c]
        n = len(cycle)

        if n <= 3 or not edges_removed[c]:
            continue

        for idx in sorted(edges_removed[c], reverse=True):
            removed_vertices.append(cycle[idx])
            del cycle[idx]

    return tuple(child), removed_vertices


def mutate(cycles):
    c1, c2 = cycles
    new_c1 = list(c1)
    new_c2 = list(c2)

    if len(new_c1) >= 2:
        i, j = random.sample(range(len(new_c1)), 2)
        new_c1[i], new_c1[j] = new_c1[j], new_c1[i]

    if len(new_c2) >= 2:
        i, j = random.sample(range(len(new_c2)), 2)
        new_c2[i], new_c2[j] = new_c2[j], new_c2[i]

    return new_c1, new_c2


def hae(distance_matrix, iterations, population=20, should_mutate=False):
    population_list = []

    while len(population_list) < population:
        new_cycles = construct_random(len(distance_matrix))
        new_cycles_local = local_search_with_move_list(
            new_cycles[0], new_cycles[1], distance_matrix
        )
        new_cycles_cost = cycles_cost(
            distance_matrix, new_cycles_local[0], new_cycles_local[1]
        )

        if all(cost != new_cycles_cost for (_, cost) in population_list):
            population_list.append((new_cycles_local, new_cycles_cost))

    for _ in range(iterations):
        parents = random.sample(population_list, 2)
        child, removed = recombine(parents)
        insertion_weighted_regret(child[0], child[1], removed, distance_matrix)
        if not child[0] or not child[1]:
            continue
        mutations = random.randrange(max(1, int(pow(len(child[0]), 0.4))))

        if should_mutate:
            for i in range(mutations):
                child = mutate(child)

        child = local_search_with_move_list(child[0], child[1], distance_matrix)

        child_cost = cycles_cost(distance_matrix, child[0], child[1])

        iterations += 1

        if any(cost == child_cost for (_, cost) in population_list):
            iterations += 1
            continue

        worst_idx, (worst_cycles, worst_cost) = max(
            enumerate(population_list), key=lambda x: x[1][1]
        )

        if child_cost < worst_cost:
            population_list[worst_idx] = (child, child_cost)

    best_cycles, _ = min(population_list, key=lambda x: x[1])

    return best_cycles
