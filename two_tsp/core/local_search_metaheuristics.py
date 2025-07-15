import random
from typing import Tuple, List

from two_tsp.core.construct import (
    construct_random,
    insertion_weighted_regret,
)
from two_tsp.core.helpers import cycles_cost
from two_tsp.core.local_search_optimized import local_search_with_move_list


def msls(
    dist: List[List[float]], num_iterations: int = 100
) -> Tuple[List[int], List[int]]:
    best_sol = None
    best_cost = float("inf")

    for _ in range(num_iterations):
        c1, c2 = construct_random(len(dist))
        ls_c1, ls_c2 = local_search_with_move_list(dist, c1, c2)
        cost = cycles_cost(dist, ls_c1, ls_c2)
        if cost < best_cost:
            best_cost = cost
            best_sol = (ls_c1, ls_c2)

    if best_sol is None:
        raise RuntimeError("No solution found.")

    return best_sol


def perturbation_ils(
    c1: List[int], c2: List[int], intensity: int = 1
) -> Tuple[List[int], List[int]]:
    new_c1, new_c2 = c1.copy(), c2.copy()

    use_first = random.random() < 0.5
    tgt = new_c1 if use_first else new_c2
    n = len(tgt)
    if n <= 1:
        return new_c1, new_c2

    k = max(1, min(intensity, n - 1))
    removed = random.sample(tgt, k)
    tgt[:] = [v for v in tgt if v not in removed]

    for v in removed:
        pos = random.randrange(len(tgt) + 1)
        tgt.insert(pos, v)

    return new_c1, new_c2


def ils(
    dist: List[List[float]],
    perturbation_intensity: int = 1,
    num_iterations: int = 100,
) -> Tuple[List[int], List[int]]:
    c1r, c2r = construct_random(len(dist))
    c1, c2 = local_search_with_move_list(dist, c1r, c2r)
    best_cost = cycles_cost(dist, c1, c2)

    for iters in range(num_iterations):
        y_c1, y_c2 = perturbation_ils(c1, c2, intensity=perturbation_intensity)
        y_c1, y_c2 = local_search_with_move_list(dist, y_c1, y_c2)
        y_cost = cycles_cost(dist, y_c1, y_c2)

        if y_cost < best_cost:
            c1, c2, best_cost = y_c1, y_c2, y_cost

    return c1, c2


def perturbation_lns(
    c1: List[int], c2: List[int], removal_rate: float = 0.3
) -> Tuple[List[int], List[int], List[int], List[int]]:
    def remove_random_vertices(cycle: List[int], k: int) -> List[int]:
        removed = set(random.sample(cycle, k))
        cycle[:] = [v for v in cycle if v not in removed]
        return list(removed)

    new_c1, new_c2 = c1.copy(), c2.copy()

    r1 = max(1, int(len(new_c1) * removal_rate))
    r2 = max(1, int(len(new_c2) * removal_rate))

    removed_c1 = remove_random_vertices(new_c1, r1)
    removed_c2 = remove_random_vertices(new_c2, r2)

    return new_c1, removed_c1, new_c2, removed_c2


def lns(
    dist: List[List[float]],
    removal_rate: float = 0.3,
    num_iterations: int = 100,
    is_local_also: bool = False,
) -> Tuple[List[int], List[int]]:
    c1, c2 = construct_random(len(dist))
    c1, c2 = local_search_with_move_list(dist, c1, c2)
    best_cost = cycles_cost(dist, c1, c2)

    for iters in range(num_iterations):
        d_c1, rem_c1, d_c2, rem_c2 = perturbation_lns(c1, c2, removal_rate)
        d_c1, d_c2 = insertion_weighted_regret(
            d_c1, d_c2, rem_c1 + rem_c2, dist, alpha=0.75
        )

        if is_local_also:
            d_c1, d_c2 = local_search_with_move_list(dist, d_c1, d_c2)

        new_cost = cycles_cost(dist, d_c1, d_c2)

        if new_cost < best_cost:
            c1, c2, best_cost = d_c1, d_c2, new_cost
    return c1, c2
