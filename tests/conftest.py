# mypy: disable-error-code=no-untyped-def
import os
import sys
import glob
import random
import pytest

from two_tsp.loader import load_instance
from two_tsp.helpers import compute_distance_matrix, cycles_cost
from two_tsp.construct import (
    greedy_nearest_neighbor,
    greedy_cycle,
    regret_cycle,
    generate_random_two_cycles,
)

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root)


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
def solvers():
    return {
        "nn": lambda dm: greedy_nearest_neighbor(dm),
        "cycle": lambda dm: greedy_cycle(dm),
        "regret": lambda dm: regret_cycle(dm, weighted=False),
        "wregret": lambda dm: regret_cycle(dm, weighted=True, alpha=0.75),
        "random": lambda dm: generate_random_two_cycles(len(dm)),
    }


@pytest.fixture(scope="session")
def instances():
    pattern = os.path.join(root, "instances", "kro", "*.tsp")
    return glob.glob(pattern)


@pytest.fixture(autouse=True)
def seed_random():
    random.seed(0)
