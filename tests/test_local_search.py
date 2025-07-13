# mypy: disable-error-code=no-untyped-def
import os
import pytest
from two_tsp.construct import generate_random_two_cycles


@pytest.mark.parametrize(
    "method_name",
    [
        "steepest_vertices",
        "steepest_edges",
        "greedy_vertices",
        "greedy_edges",
        "random_walk",
    ],
)
def test_local_search_improves(
    method_name,
    load_instance_fn,
    compute_distance_matrix_fn,
    cycles_cost_fn,
    local_search_solvers,
    instances,
):
    method = local_search_solvers[method_name]
    for tsp_file in instances:
        coords = load_instance_fn(tsp_file)
        dm = compute_distance_matrix_fn(coords)
        initial_c1, initial_c2 = generate_random_two_cycles(len(dm))
        new_c1, new_c2 = method(initial_c1, initial_c2, dm)

        n = len(dm)
        all_nodes = set(range(n))

        assert set(new_c1).isdisjoint(
            new_c2
        ), f"{method_name}: overlap on {os.path.basename(tsp_file)}"
        assert (
            set(new_c1) | set(new_c2) == all_nodes
        ), f"{method_name}: coverage on {os.path.basename(tsp_file)}"
        assert (
            abs(len(new_c1) - len(new_c2)) <= 1
        ), f"{method_name}: Cycles are of different length on {os.path.basename(tsp_file)}"

        cost_initial = cycles_cost_fn(dm, initial_c1, initial_c2)
        cost_new = cycles_cost_fn(dm, new_c1, new_c2)
        assert cost_new <= cost_initial, (
            f"{method_name}: cost worsened ({cost_new} > {cost_initial}) "
            f"on {os.path.basename(tsp_file)}"
        )
