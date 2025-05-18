import math
from typing import Sequence, List

import tsplib95


def load_instance(file_name: str):
    problem = tsplib95.load(file_name)
    coordinates = [coord for _, coord in sorted(problem.node_coords.items())]
    return coordinates

def compute_distance_matrix(coordinates):
    n = len(coordinates)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dx = coordinates[i][0] - coordinates[j][0]
            dy = coordinates[i][1] - coordinates[j][1]
            dist = int(round(math.sqrt(dx * dx + dy * dy)))
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix


def _d(a: int, b: int, dist: Sequence[Sequence[float]]) -> float:
    return dist[a][b]

def cycle_cost(cycle: Sequence[int], dist: Sequence[Sequence[float]]) -> float:
    n = len(cycle)
    return sum(_d(cycle[i], cycle[(i + 1) % n], dist) for i in range(n))

def total_cost(
    c1: Sequence[int],
    c2: Sequence[int],
    dist: Sequence[Sequence[float]],
) -> float:
    return cycle_cost(c1, dist) + cycle_cost(c2, dist)

def delta_2opt(
    cycle: Sequence[int],
    i: int,
    j: int,
    dist: Sequence[Sequence[float]],
) -> float:
    n = len(cycle)
    a, b = cycle[i], cycle[(i + 1) % n]
    c, d = cycle[j], cycle[(j + 1) % n]
    old = _d(a, b, dist) + _d(c, d, dist)
    new = _d(a, c, dist) + _d(b, d, dist)
    return new - old

def delta_v_between(
    c1: Sequence[int],
    c2: Sequence[int],
    i: int,
    j: int,
    dist: Sequence[Sequence[float]],
) -> float:
    n1, n2 = len(c1), len(c2)
    a_prev, a, a_next = c1[(i - 1) % n1], c1[i], c1[(i + 1) % n1]
    b_prev, b, b_next = c2[(j - 1) % n2], c2[j], c2[(j + 1) % n2]

    old = (
        _d(a_prev, a, dist)
        + _d(a, a_next, dist)
        + _d(b_prev, b, dist)
        + _d(b, b_next, dist)
    )
    new = (
        _d(a_prev, b, dist)
        + _d(b, a_next, dist)
        + _d(b_prev, a, dist)
        + _d(a, b_next, dist)
    )
    return new - old

def delta_vertex(
    cycle: Sequence[int],
    i: int,
    j: int,
    dist: Sequence[Sequence[float]],
) -> float:

    if i == j:
        return 0.0

    n = len(cycle)

    if i > j:
        i, j = j, i

    vi = cycle[i]
    vj = cycle[j]

    vi_prev = cycle[(i - 1) % n]
    vi_next = cycle[(i + 1) % n]
    vj_prev = cycle[(j - 1) % n]
    vj_next = cycle[(j + 1) % n]

    if (i + 1) % n == j:
        old = dist[vi_prev][vi] + dist[vi][vj] + dist[vj][vj_next]
        new = dist[vi_prev][vj] + dist[vj][vi] + dist[vi][vj_next]
        return new - old

    if (j + 1) % n == i:
        old = dist[vj_prev][vj] + dist[vj][vi] + dist[vi][vi_next]
        new = dist[vj_prev][vi] + dist[vi][vj] + dist[vj][vi_next]
        return new - old

    old = (
        dist[vi_prev][vi] + dist[vi][vi_next] +
        dist[vj_prev][vj] + dist[vj][vj_next]
    )
    new = (
        dist[vi_prev][vj] + dist[vj][vi_next] +
        dist[vj_prev][vi] + dist[vi][vj_next]
    )
    return new - old


def apply_2opt(cycle: List[int], i: int, j: int) -> List[int]:
    return cycle[: i+1] + list(reversed(cycle[i+1 : j+1])) + cycle[j+1 :]

def apply_v_between(c1: List[int], c2: List[int], i: int, j: int):
    c1[i], c2[j] = c2[j], c1[i]
