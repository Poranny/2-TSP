import random
from helpers import cycle_cost

def greedy_nearest_neighbor(distance_matrix):
    n = len(distance_matrix)
    if n == 0:
        return ([], [], 0)

    all_vertices = set(range(n))
    start1 = random.choice(list(all_vertices))
    all_vertices.remove(start1)

    if all_vertices:
        start2 = max(all_vertices, key=lambda v: distance_matrix[start1][v])
        all_vertices.remove(start2)
    else:
        start2 = None

    cycle1 = [start1]
    cycle2 = [start2] if start2 is not None else []

    turn = 0
    while all_vertices:
        if turn == 0:
            last = cycle1[-1]
            next_v = min(all_vertices, key=lambda v: distance_matrix[last][v])
            cycle1.append(next_v)
            all_vertices.remove(next_v)
        else:
            last = cycle2[-1]
            next_v = min(all_vertices, key=lambda v: distance_matrix[last][v])
            cycle2.append(next_v)
            all_vertices.remove(next_v)
        turn = 1 - turn

    total_cost = cycle_cost(distance_matrix, cycle1) + cycle_cost(distance_matrix, cycle2)
    return cycle1, cycle2, total_cost


def greedy_cycle(distance_matrix):
    n = len(distance_matrix)
    if n == 0:
        return ([], [], 0)

    vertices = set(range(n))
    start1 = random.choice(list(vertices))
    vertices.remove(start1)
    second1 = min(vertices, key=lambda v: distance_matrix[start1][v])
    vertices.remove(second1)
    cycle1 = [start1, second1]

    if vertices:
        start2 = max(vertices, key=lambda v: distance_matrix[start1][v])
        vertices.remove(start2)
        if vertices:
            second2 = min(vertices, key=lambda v: distance_matrix[start2][v])
            vertices.remove(second2)
            cycle2 = [start2, second2]
        else:
            cycle2 = [start2]
    else:
        cycle2 = []

    def insertion_cost(cycle, i, v):
        j = (i + 1) % len(cycle)
        return (distance_matrix[cycle[i]][v]
                + distance_matrix[v][cycle[j]]
                - distance_matrix[cycle[i]][cycle[j]])

    turn = 0
    while vertices:
        best_increase = float('inf')
        current_cycle = cycle1 if turn == 0 else cycle2

        best_index = None
        best_vertex = None

        for i in range(len(current_cycle)):
            for v in vertices:
                cost_inc = insertion_cost(current_cycle, i, v)
                if cost_inc < best_increase:
                    best_increase = cost_inc
                    best_cycle = current_cycle
                    best_index = i + 1
                    best_vertex = v

        best_cycle.insert(best_index, best_vertex)
        vertices.remove(best_vertex)
        turn = 1 - turn

    total_cost = cycle_cost(distance_matrix, cycle1) + cycle_cost(distance_matrix, cycle2)
    return cycle1, cycle2, total_cost


def regret_cycle(distance_matrix, weighted, alpha=1.0):
    n = len(distance_matrix)
    if n == 0:
        return ([], [], 0)

    vertices = set(range(n))
    start1 = random.choice(list(vertices))
    vertices.remove(start1)
    second1 = min(vertices, key=lambda v: distance_matrix[start1][v])
    vertices.remove(second1)
    cycle1 = [start1, second1]

    if vertices:
        start2 = max(vertices, key=lambda v: distance_matrix[start1][v])
        vertices.remove(start2)
        if vertices:
            second2 = min(vertices, key=lambda v: distance_matrix[start2][v])
            vertices.remove(second2)
            cycle2 = [start2, second2]
        else:
            cycle2 = [start2]
    else:
        cycle2 = []

    turn = 0
    while vertices:
        candidates = []
        current_cycle = cycle1 if turn == 0 else cycle2
        m = len(current_cycle)

        for v in vertices:
            costs = []
            for i in range(m):
                j = (i + 1) % m
                cost = (distance_matrix[current_cycle[i]][v]
                        + distance_matrix[v][current_cycle[j]]
                        - distance_matrix[current_cycle[i]][current_cycle[j]])
                costs.append((cost, i + 1))
            costs.sort(key=lambda x: x[0])
            best_cost, best_pos = costs[0]
            second_cost = costs[1][0] if len(costs) > 1 else best_cost
            regret = second_cost - best_cost
            if weighted:
                regret = alpha * regret - (1 - alpha) * best_cost
            candidates.append((regret, best_cost, current_cycle, best_pos, v))

        if not candidates:
            break

        _, _, chosen_cycle, pos, chosen_vertex = max(candidates, key=lambda x: x[0])
        chosen_cycle.insert(pos, chosen_vertex)
        vertices.remove(chosen_vertex)
        turn = 1 - turn

    total_cost = cycle_cost(distance_matrix, cycle1) + cycle_cost(distance_matrix, cycle2)
    return cycle1, cycle2, total_cost


