# mypy: disable-error-code=no-untyped-def
import pytest


@pytest.mark.parametrize("mutate_flag", [False, True])
def test_hae_validity_and_cost(
    mutate_flag: bool,
    load_instance_fn,
    compute_distance_matrix_fn,
    construct_solvers,
    cycles_cost_fn,
    evo_solvers,
    instances,
):
    hae_fn = evo_solvers["hae"]

    ITERATIONS = 25
    POPULATION = 10

    for tsp_file in instances:
        coords = load_instance_fn(tsp_file)
        dm = compute_distance_matrix_fn(coords)

        base_c1, base_c2 = construct_solvers["random"](dm)
        base_cost = cycles_cost_fn(dm, base_c1, base_c2)

        c1, c2 = hae_fn(
            dm,
            iterations=ITERATIONS,
            population=POPULATION,
            should_mutate=mutate_flag,
        )
        cost = cycles_cost_fn(dm, c1, c2)

        n = len(coords)
        all_nodes = set(range(n))

        assert set(c1).isdisjoint(c2), f"HAE {mutate_flag}: overlap on {tsp_file}"
        assert (
            set(c1) | set(c2)
        ) == all_nodes, f"HAE {mutate_flag}: coverage on {tsp_file}"
        assert (
            abs(len(c1) - len(c2)) <= 1
        ), f"HAE {mutate_flag}: uneven length on {tsp_file}"

        assert (
            cost <= base_cost
        ), f"HAE {mutate_flag}: cost {cost} > baseline {base_cost} on {tsp_file}"
