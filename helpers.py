import math

import tsplib95


def load_instance(file_name: str):
    problem = tsplib95.load(file_name)
    coordinates = [coord for _, coord in sorted(problem.node_coords.items())]
    return coordinates


def compute_distance_matrix(coordinates):
    n = len(coordinates)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dx = coordinates[i][0] - coordinates[j][0]
            dy = coordinates[i][1] - coordinates[j][1]
            dist = int(round(math.sqrt(dx * dx + dy * dy)))
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix


def cycle_cost(distance_matrix, cycle):
    cost = sum(distance_matrix[cycle[i]][cycle[i + 1]] for i in range(len(cycle) - 1))
    cost += distance_matrix[cycle[-1]][cycle[0]]
    return cost
