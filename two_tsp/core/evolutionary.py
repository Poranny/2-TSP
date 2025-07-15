from __future__ import annotations

import random
from typing import List, Tuple, Sequence, Set

from two_tsp.core.construct import construct_random, insertion_weighted_regret
from two_tsp.core.helpers import cycles_cost
from two_tsp.core.local_search_optimized import local_search_with_move_list


def recombine(
    parents: Sequence[Tuple[Tuple[List[int], List[int]], float]],
) -> Tuple[Tuple[List[int], List[int]], List[int]]:
    parent1, parent2 = parents[0][0], parents[1][0]

    edges_removed_pos1: List[Tuple[int, int]] = []
    removed_vertices: List[int] = []

    for c in range(2):
        cycle1 = parent1[c]
        n = len(cycle1)
        for i in range(n):
            v, v_next = cycle1[i], cycle1[(i + 1) % n]
            edge_exists = False
            for c2 in range(2):
                cycle2 = parent2[c2]
                m = len(cycle2)
                for j in range(m):
                    u, u_next = cycle2[j], cycle2[(j + 1) % m]
                    if (v == u and v_next == u_next) or (v == u_next and v_next == u):
                        edge_exists = True
                        break
                if edge_exists:
                    break
            if not edge_exists:
                edges_removed_pos1.append((c, i))

    child: List[List[int]] = [list(parent1[0]), list(parent1[1])]
    edges_removed: List[Set[int]] = [set(), set()]
    for c, i in edges_removed_pos1:
        n = len(child[c])
        edges_removed[c].update({i, (i + 1) % n})

    for c in range(2):
        cycle = child[c]
        if len(cycle) <= 3 or not edges_removed[c]:
            continue
        for idx in sorted(edges_removed[c], reverse=True):
            removed_vertices.append(cycle[idx])
            del cycle[idx]

    return (child[0], child[1]), removed_vertices


def mutate(cycles: Tuple[List[int], List[int]]) -> Tuple[List[int], List[int]]:
    c1, c2 = cycles
    new_c1, new_c2 = list(c1), list(c2)

    if len(new_c1) >= 2:
        i, j = random.sample(range(len(new_c1)), 2)
        new_c1[i], new_c1[j] = new_c1[j], new_c1[i]

    if len(new_c2) >= 2:
        i, j = random.sample(range(len(new_c2)), 2)
        new_c2[i], new_c2[j] = new_c2[j], new_c2[i]

    return new_c1, new_c2


def hae(
    distance_matrix: List[List[float]],
    iterations: int,
    population: int = 20,
    should_mutate: bool = True,
) -> Tuple[List[int], List[int]]:

    population_list: List[Tuple[Tuple[List[int], List[int]], float]] = []

    while len(population_list) < population:
        cycles = construct_random(len(distance_matrix))
        cycles_ls = local_search_with_move_list(cycles[0], cycles[1], distance_matrix)
        cost = cycles_cost(distance_matrix, cycles_ls[0], cycles_ls[1])
        if all(cost != c for (_, c) in population_list):
            population_list.append((cycles_ls, cost))

    for _ in range(iterations):
        parents = random.sample(population_list, 2)
        child, removed = recombine(parents)

        insertion_weighted_regret(child[0], child[1], removed, distance_matrix)

        if not child[0] or not child[1]:
            continue

        mut_range = max(1, int(len(child[0]) ** 0.4))
        if should_mutate:
            for _ in range(random.randrange(mut_range)):
                child = mutate(child)

        child = local_search_with_move_list(child[0], child[1], distance_matrix)
        child_cost = cycles_cost(distance_matrix, child[0], child[1])

        if any(c == child_cost for (_, c) in population_list):
            continue

        worst_idx, (_, worst_cost) = max(
            enumerate(population_list), key=lambda x: x[1][1]
        )
        if child_cost < worst_cost:
            population_list[worst_idx] = (child, child_cost)

    best_cycles, _ = min(population_list, key=lambda x: x[1])
    return best_cycles
