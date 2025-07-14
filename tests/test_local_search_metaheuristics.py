# mypy: disable-error-code=no-untyped-def
import pytest


@pytest.mark.parametrize("baseline_name", ["random"])
def test_local_search_metaheuristics_validity_and_cost(
    baseline_name: str,
    load_instance_fn,
    compute_distance_matrix_fn,
    construct_solvers,
    cycles_cost_fn,
    instances,
    local_search_meta_solvers,
):

    for tsp_file in instances:
        coords = load_instance_fn(tsp_file)
        dm = compute_distance_matrix_fn(coords)

        base_c1, base_c2 = construct_solvers[baseline_name](dm)
        base_cost = cycles_cost_fn(dm, base_c1, base_c2)

        n = len(coords)
        all_nodes = set(range(n))

        for meta_name, meta_fn in local_search_meta_solvers.items():
            c1, c2 = meta_fn(coords, dm)
            cost = cycles_cost_fn(dm, c1, c2)

            assert set(c1).isdisjoint(c2), f"{meta_name}: overlap on {tsp_file}"
            assert (
                set(c1) | set(c2)
            ) == all_nodes, f"{meta_name}: coverage on {tsp_file}"
            assert (
                abs(len(c1) - len(c2)) <= 1
            ), f"{meta_name}: length diff on {tsp_file}"

            assert (
                cost <= base_cost
            ), f"{meta_name}: cost {cost} > baseline {base_cost} on {tsp_file}"
