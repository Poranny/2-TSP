# mypy: disable-error-code=no-untyped-def
import glob
import random
from pathlib import Path

import pytest

from two_tsp.loader import load_instance
from two_tsp.helpers import compute_distance_matrix, cycles_cost
from two_tsp.construct import (
    construct_nearest_neighbour,
    construct_greedy_cycle,
    construct_weighted_regret,
    construct_random,
)
from two_tsp.local_search import (
    local_steepest_vertices,
    local_steepest_edges,
    local_greedy_vertices,
    local_greedy_edges,
    random_walk,
)
from two_tsp.local_search_optimized import (
    local_search_with_move_list,
    local_search_with_candidates,
)


@pytest.fixture(scope="session")
def load_instance_fn():
    return load_instance


@pytest.fixture(scope="session")
def compute_distance_matrix_fn():
    return compute_distance_matrix


@pytest.fixture(scope="session")
def cycles_cost_fn():
    return cycles_cost


@pytest.fixture(scope="session")
def construct_solvers():
    return {
        "nn": lambda dm: construct_nearest_neighbour(dm),
        "cycle": lambda dm: construct_greedy_cycle(dm),
        "regret": lambda dm: construct_weighted_regret(dm, weighted=False),
        "wregret": lambda dm: construct_weighted_regret(dm, weighted=True, alpha=0.75),
        "random": lambda dm: construct_random(len(dm)),
    }


@pytest.fixture(scope="session")
def local_search_solvers():
    return {
        "steepest_vertices": local_steepest_vertices,
        "steepest_edges": local_steepest_edges,
        "greedy_vertices": local_greedy_vertices,
        "greedy_edges": local_greedy_edges,
        "random_walk": random_walk,
    }


@pytest.fixture(scope="session")
def local_search_optimized_solvers():
    return {
        "move_list": local_search_with_move_list,
        "candidates": local_search_with_candidates,
    }


@pytest.fixture(scope="session")
def instances():
    repo_root = Path(__file__).resolve().parents[1]
    tsp_path = repo_root / "tests" / "test_instances" / "*.tsp"
    return glob.glob(str(tsp_path))


@pytest.fixture(autouse=True)
def seed_random():
    random.seed(0)
