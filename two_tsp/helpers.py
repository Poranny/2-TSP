import math
from typing import List, Tuple


def compute_distance_matrix(coordinates: List[tuple[float, float]]) -> List[List[int]]:
    n = len(coordinates)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        x_i, y_i = coordinates[i]
        for j in range(i + 1, n):
            x_j, y_j = coordinates[j]
            dx, dy = x_i - x_j, y_i - y_j
            d = int(round(math.hypot(dx, dy)))
            matrix[i][j] = matrix[j][i] = d
    return matrix


def cycle_cost(distance_matrix: List[List[int]], cycle: List[int]) -> int:
    cost = 0
    for i in range(len(cycle) - 1):
        cost += distance_matrix[cycle[i]][cycle[i + 1]]
    cost += distance_matrix[cycle[-1]][cycle[0]]
    return cost


def cycles_cost(
    distance_matrix: List[List[int]], cycle1: List[int], cycle2: List[int]
) -> int:
    return cycle_cost(distance_matrix, cycle1) + cycle_cost(distance_matrix, cycle2)

def delta_vertex(distance_matrix: List[List[int]], cycle: List[int], i: int, j: int) -> int:
    before = cycle_cost(distance_matrix, cycle)
    cycle[i], cycle[j] = cycle[j], cycle[i]
    after = cycle_cost(distance_matrix, cycle)
    cycle[i], cycle[j] = cycle[j], cycle[i]
    return after - before

def delta_edge(distance_matrix: List[List[int]], cycle: List[int], i: int, j: int) -> int:
    before = cycle_cost(distance_matrix, cycle)
    new_cycle = cycle[: i + 1] + list(reversed(cycle[i + 1 : j + 1])) + cycle[j + 1 :]
    after = cycle_cost(distance_matrix, new_cycle)
    return after - before

def delta_2opt(
    distance_matrix: List[List[int]], cycle: List[int], i: int, j: int
) -> int:
    n = len(cycle)
    a, b = cycle[i], cycle[(i + 1) % n]
    c, d = cycle[j], cycle[(j + 1) % n]
    removal = distance_matrix[a][b] + distance_matrix[c][d]
    addition = distance_matrix[a][c] + distance_matrix[b][d]
    return addition - removal

def apply_2opt(cycle: List[int], i: int, j: int) -> List[int]:
    return cycle[: i + 1] + list(reversed(cycle[i + 1 : j + 1])) + cycle[j + 1 :]

def delta_between(
    distance_matrix: List[List[int]],
    cycle1: List[int],
    cycle2: List[int],
    i: int,
    j: int,
) -> int:
    n1, n2 = len(cycle1), len(cycle2)
    v1, v2 = cycle1[i], cycle2[j]
    p1, n1p = cycle1[i - 1], cycle1[(i + 1) % n1]
    p2, n2p = cycle2[j - 1], cycle2[(j + 1) % n2]
    before = distance_matrix[p1][v1] + distance_matrix[v1][n1p] + distance_matrix[p2][v2] + distance_matrix[v2][n2p]
    after = distance_matrix[p1][v2] + distance_matrix[v2][n1p] + distance_matrix[p2][v1] + distance_matrix[v1][n2p]
    return after - before

def apply_between(
    cycle1: List[int], cycle2: List[int], i: int, j: int
) -> None:
    cycle1[i], cycle2[j] = cycle2[j], cycle1[i]

def find_nearest_neighbors(
    distance_matrix: List[List[int]], k: int = 10
) -> List[List[int]]:
    n = len(distance_matrix)
    result: List[List[int]] = []
    for i in range(n):
        distances = sorted(
            ((j, distance_matrix[i][j]) for j in range(n) if j != i),
            key=lambda x: x[1],
        )
        result.append([j for j, _ in distances[:k]])
    return result

def is_edge_in_same_orientation(cycle: List[int], edge: Tuple[int, int]) -> bool:
    n = len(cycle)
    for idx in range(n):
        if cycle[idx] == edge[0] and cycle[(idx + 1) % n] == edge[1]:
            return True
    return False

def check_all_edges(
    cycle: List[int], edges: List[Tuple[int, int]]
) -> int:
    any_reversed = False
    for e in edges:
        if is_edge_in_same_orientation(cycle, e):
            continue
        if is_edge_in_same_orientation(cycle, (e[1], e[0])):
            any_reversed = True
        else:
            return 0
    return 1 if any_reversed else 2

def check_all_edges_two_cycles(
    c1: List[int],
    c2: List[int],
    edges_c1: List[Tuple[int, int]],
    edges_c2: List[Tuple[int, int]],
) -> int:
    r1 = check_all_edges(c1, edges_c1)
    if r1 == 0:
        return 0
    r2 = check_all_edges(c2, edges_c2)
    if r2 == 0:
        return 0
    return 1 if (r1 == 1 or r2 == 1) else 2