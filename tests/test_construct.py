# mypy: disable-error-code=no-untyped-def
import os
import pytest


@pytest.mark.parametrize("solver_name", ["nn", "cycle", "regret", "wregret"])
def test_solution_validity(
    solver_name,
    load_instance_fn,
    compute_distance_matrix_fn,
    construct_solvers,
    instances,
) -> None:
    for tsp_file in instances:
        coords = load_instance_fn(tsp_file)
        dm = compute_distance_matrix_fn(coords)
        c1, c2 = construct_solvers[solver_name](dm)

        n = len(coords)
        all_nodes = set(range(n))

        assert set(c1).isdisjoint(
            c2
        ), f"{solver_name}: Cycles overlap on {os.path.basename(tsp_file)}"
        assert (
            set(c1) | set(c2) == all_nodes
        ), f"{solver_name}: Not all nodes covered on {os.path.basename(tsp_file)}"
        assert (
            abs(len(c1) - len(c2)) <= 1
        ), f"{solver_name}: Cycles are of different length on {os.path.basename(tsp_file)}"


@pytest.mark.parametrize("solver_name", ["nn", "cycle", "regret", "wregret"])
def test_heuristic_better_than_random(
    solver_name,
    load_instance_fn,
    compute_distance_matrix_fn,
    construct_solvers,
    instances,
    cycles_cost_fn,
) -> None:
    random_solver = construct_solvers["random"]
    heuristic_solver = construct_solvers[solver_name]

    for tsp_file in instances:
        coords = load_instance_fn(tsp_file)
        dm = compute_distance_matrix_fn(coords)

        h_c1, h_c2 = heuristic_solver(dm)
        r_c1, r_c2 = random_solver(dm)

        h_cost = cycles_cost_fn(dm, h_c1, h_c2)
        r_cost = cycles_cost_fn(dm, r_c1, r_c2)

        assert h_cost < r_cost, (
            f"{solver_name}: heuristic cost {h_cost} ≥ random cost {r_cost} "
            f"for instance {os.path.basename(tsp_file)}"
        )
