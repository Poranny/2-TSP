import random
import time
from typing import List, Tuple
from two_tsp.core.helpers import cycles_cost, delta_vertex, delta_edge


def local_steepest_vertices(
    cycle1: List[int], cycle2: List[int], dm: List[List[float]]
) -> Tuple[List[int], List[int]]:
    c1 = cycle1[:]
    c2 = cycle2[:]
    while True:
        best_delta = 0.0
        best_move = None
        for i in range(len(c1)):
            for j in range(i + 1, len(c1)):
                d = delta_vertex(dm, c1, i, j)
                if d < best_delta:
                    best_delta = d
                    best_move = (1, i, j)
        for i in range(len(c2)):
            for j in range(i + 1, len(c2)):
                d = delta_vertex(dm, c2, i, j)
                if d < best_delta:
                    best_delta = d
                    best_move = (2, i, j)
        if best_move is None:
            break
        which, i, j = best_move
        if which == 1:
            c1[i], c1[j] = c1[j], c1[i]
        else:
            c2[i], c2[j] = c2[j], c2[i]
    return c1, c2


def local_steepest_edges(
    cycle1: List[int], cycle2: List[int], dm: List[List[float]]
) -> Tuple[List[int], List[int]]:
    c1 = cycle1[:]
    c2 = cycle2[:]
    while True:
        best_delta = 0.0
        best_move = None
        for i in range(len(c1)):
            for j in range(i + 2, len(c1)):
                d = delta_edge(dm, c1, i, j)
                if d < best_delta:
                    best_delta = d
                    best_move = (1, i, j)
        for i in range(len(c2)):
            for j in range(i + 2, len(c2)):
                d = delta_edge(dm, c2, i, j)
                if d < best_delta:
                    best_delta = d
                    best_move = (2, i, j)
        if best_move is None:
            break
        which, i, j = best_move
        if which == 1:
            c1 = c1[: i + 1] + list(reversed(c1[i + 1 : j + 1])) + c1[j + 1 :]
        else:
            c2 = c2[: i + 1] + list(reversed(c2[i + 1 : j + 1])) + c2[j + 1 :]
    return c1, c2


def local_greedy_vertices(
    cycle1: List[int], cycle2: List[int], dm: List[List[float]]
) -> Tuple[List[int], List[int]]:
    c1 = cycle1[:]
    c2 = cycle2[:]
    improved = True
    while improved:
        improved = False
        pairs = []
        for i in range(len(c1)):
            for j in range(i + 1, len(c1)):
                pairs.append((1, i, j))
        for i in range(len(c2)):
            for j in range(i + 1, len(c2)):
                pairs.append((2, i, j))
        random.shuffle(pairs)
        for which, i, j in pairs:
            if which == 1:
                d = delta_vertex(dm, c1, i, j)
                if d < 0.0:
                    c1[i], c1[j] = c1[j], c1[i]
                    improved = True
                    break
            else:
                d = delta_vertex(dm, c2, i, j)
                if d < 0.0:
                    c2[i], c2[j] = c2[j], c2[i]
                    improved = True
                    break
    return c1, c2


def local_greedy_edges(
    cycle1: List[int], cycle2: List[int], dm: List[List[float]]
) -> Tuple[List[int], List[int]]:
    c1 = cycle1[:]
    c2 = cycle2[:]
    improved = True
    while improved:
        improved = False
        pairs = []
        for i in range(len(c1)):
            for j in range(i + 2, len(c1)):
                pairs.append((1, i, j))
        for i in range(len(c2)):
            for j in range(i + 2, len(c2)):
                pairs.append((2, i, j))
        random.shuffle(pairs)
        for which, i, j in pairs:
            if which == 1:
                d = delta_edge(dm, c1, i, j)
                if d < 0.0:
                    c1 = c1[: i + 1] + list(reversed(c1[i + 1 : j + 1])) + c1[j + 1 :]
                    improved = True
                    break
            else:
                d = delta_edge(dm, c2, i, j)
                if d < 0.0:
                    c2 = c2[: i + 1] + list(reversed(c2[i + 1 : j + 1])) + c2[j + 1 :]
                    improved = True
                    break
    return c1, c2


def random_walk(
    cycle1: List[int], cycle2: List[int], dm: List[List[float]], time_limit: float = 1.0
) -> Tuple[List[int], List[int]]:
    start = time.time()
    c1 = cycle1[:]
    c2 = cycle2[:]
    best_c1 = c1[:]
    best_c2 = c2[:]
    best_cost = cycles_cost(dm, c1, c2)
    while time.time() - start < time_limit:
        move = random.choice([1, 2, 3])
        if move == 1 and len(c1) > 1:
            i, j = random.sample(range(len(c1)), 2)
            c1[i], c1[j] = c1[j], c1[i]
        elif move == 2 and len(c2) > 1:
            i, j = random.sample(range(len(c2)), 2)
            c2[i], c2[j] = c2[j], c2[i]
        else:
            if len(c1) > 0 and len(c2) > 0:
                i = random.randrange(len(c1))
                j = random.randrange(len(c2))
                c1[i], c2[j] = c2[j], c1[i]
        cost = cycles_cost(dm, c1, c2)
        if cost < best_cost:
            best_cost = cost
            best_c1 = c1[:]
            best_c2 = c2[:]
    return best_c1, best_c2
