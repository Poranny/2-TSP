# mypy: disable-error-code=no-untyped-def
import time
import pytest

from two_tsp.core.local_search import local_steepest_edges
from two_tsp.core.local_search_optimized import (
    local_search_with_move_list,
    local_search_with_candidates,
)


@pytest.mark.parametrize(
    "opt_name,opt_fn",
    [
        ("move_list", local_search_with_move_list),
        ("candidates", local_search_with_candidates),
    ],
)
def test_local_search_optimized_validity_and_cost(
    opt_name: str,
    opt_fn,
    load_instance_fn,
    compute_distance_matrix_fn,
    construct_solvers,
    cycles_cost_fn,
    instances,
):
    for tsp_file in instances:
        coords = load_instance_fn(tsp_file)
        dm = compute_distance_matrix_fn(coords)

        c1, c2 = construct_solvers["regret"](dm)
        cost_before = cycles_cost_fn(dm, c1, c2)

        c1_opt, c2_opt = opt_fn(dm, c1, c2)
        cost_after = cycles_cost_fn(dm, c1_opt, c2_opt)

        n = len(coords)
        all_nodes = set(range(n))

        assert set(c1_opt).isdisjoint(c2_opt), f"{opt_name}: overlap on {tsp_file}"
        assert (
            set(c1_opt) | set(c2_opt)
        ) == all_nodes, f"{opt_name}: coverage on {tsp_file}"
        assert (
            abs(len(c1_opt) - len(c2_opt)) <= 1
        ), f"{opt_name}: Cycles are of different length on {tsp_file}"

        assert (
            cost_after <= cost_before
        ), f"{opt_name}: cost did not improve ({cost_before} → {cost_after}) on {tsp_file}"


def test_local_search_optimized_performance(
    load_instance_fn,
    compute_distance_matrix_fn,
    construct_solvers,
    cycles_cost_fn,
    instances,
    local_search_optimized_solvers,
):
    for tsp_file in instances:
        coords = load_instance_fn(tsp_file)
        dm = compute_distance_matrix_fn(coords)
        c1, c2 = construct_solvers["regret"](dm)

        t0 = time.perf_counter()
        _, _ = local_steepest_edges(c1[:], c2[:], dm)
        t_std = time.perf_counter() - t0

        for name, fn in local_search_optimized_solvers.items():
            t0 = time.perf_counter()
            c1_opt, c2_opt = fn(dm, c1[:], c2[:])
            t_opt = time.perf_counter() - t0
            cost_opt = cycles_cost_fn(dm, c1_opt, c2_opt)
            cost_base = cycles_cost_fn(dm, c1, c2)

            n = len(coords)
            assert set(c1_opt).isdisjoint(c2_opt)
            assert (set(c1_opt) | set(c2_opt)) == set(range(n))

            assert (
                cost_opt <= cost_base
            ), f"{name}: cost {cost_opt} > baseline {cost_base} on {tsp_file}"
            assert (
                t_opt <= t_std
            ), f"{name}: too slow {t_opt:.4f}s vs baseline {t_std:.4f}s on {tsp_file}"
