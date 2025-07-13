import random
from typing import List, Tuple


def generate_random_two_cycles(n: int) -> Tuple[List[int], List[int]]:
    indices = list(range(n))
    random.shuffle(indices)
    half = n // 2
    cycle1 = indices[:half]
    cycle2 = indices[half:]
    return cycle1, cycle2


def greedy_nearest_neighbor(
    distance_matrix: List[List[int]],
) -> Tuple[List[int], List[int]]:
    n = len(distance_matrix)
    if n == 0:
        return [], []
    all_v = set(range(n))
    start1 = random.choice(tuple(all_v))
    all_v.remove(start1)
    start2 = None
    if all_v:
        start2 = max(all_v, key=lambda v: distance_matrix[start1][v])
        all_v.remove(start2)
    cycle1 = [start1]
    cycle2 = [start2] if start2 is not None else []
    turn = 0
    while all_v:
        last = cycle1[-1] if turn == 0 else cycle2[-1]
        next_v = min(all_v, key=lambda v: distance_matrix[last][v])
        if turn == 0:
            cycle1.append(next_v)
        else:
            cycle2.append(next_v)
        all_v.remove(next_v)
        turn ^= 1
    return cycle1, cycle2


def greedy_cycle(distance_matrix: List[List[int]]) -> Tuple[List[int], List[int]]:
    n = len(distance_matrix)
    if n == 0:
        return [], []
    verts = set(range(n))
    s1 = random.choice(tuple(verts))
    verts.remove(s1)
    s1b = min(verts, key=lambda v: distance_matrix[s1][v])
    verts.remove(s1b)
    cycle1 = [s1, s1b]
    if verts:
        s2 = max(verts, key=lambda v: distance_matrix[s1][v])
        verts.remove(s2)
        if verts:
            s2b = min(verts, key=lambda v: distance_matrix[s2][v])
            verts.remove(s2b)
            cycle2 = [s2, s2b]
        else:
            cycle2 = [s2]
    else:
        cycle2 = []

    def ins_cost(cycle, i, v):
        j = (i + 1) % len(cycle)
        return (
            distance_matrix[cycle[i]][v]
            + distance_matrix[v][cycle[j]]
            - distance_matrix[cycle[i]][cycle[j]]
        )

    turn = 0
    while verts:
        current = cycle1 if turn == 0 else cycle2
        best_inc = float("inf")
        best = (None, None, None)
        for i in range(len(current)):
            for v in verts:
                inc = ins_cost(current, i, v)
                if inc < best_inc:
                    best_inc = inc
                    best = (current, i + 1, v)
        cyc, idx, vert = best
        cyc.insert(idx, vert)
        verts.remove(vert)
        turn ^= 1
    return cycle1, cycle2


def regret_cycle(
    distance_matrix: List[List[int]], weighted: bool, alpha: float = 0.75
) -> Tuple[List[int], List[int]]:
    n = len(distance_matrix)
    if n == 0:
        return [], []
    verts = set(range(n))
    s1 = random.choice(tuple(verts))
    verts.remove(s1)
    s1b = min(verts, key=lambda v: distance_matrix[s1][v])
    verts.remove(s1b)
    cycle1 = [s1, s1b]
    if verts:
        s2 = max(verts, key=lambda v: distance_matrix[s1][v])
        verts.remove(s2)
        if verts:
            s2b = min(verts, key=lambda v: distance_matrix[s2][v])
            verts.remove(s2b)
            cycle2 = [s2, s2b]
        else:
            cycle2 = [s2]
    else:
        cycle2 = []
    turn = 0
    while verts:
        current = cycle1 if turn == 0 else cycle2
        m = len(current)
        candidates = []
        for v in verts:
            costs = []
            for i in range(m):
                j = (i + 1) % m
                delta = (
                    distance_matrix[current[i]][v]
                    + distance_matrix[v][current[j]]
                    - distance_matrix[current[i]][current[j]]
                )
                costs.append((delta, i + 1))
            costs.sort(key=lambda x: x[0])
            best_c, pos = costs[0]
            second = costs[1][0] if len(costs) > 1 else best_c
            regret = (
                (alpha * (second - best_c) - (1 - alpha) * best_c)
                if weighted
                else (second - best_c)
            )
            candidates.append((regret, pos, v))
        sel = max(candidates, key=lambda x: x[0])
        _, pos, vtx = sel
        current.insert(pos, vtx)
        verts.remove(vtx)
        turn ^= 1
    return cycle1, cycle2
