import math
from typing import List

def compute_distance_matrix(coordinates: List[tuple]) -> List[List[int]]:
    n = len(coordinates)
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        x_i, y_i = coordinates[i]
        for j in range(i+1, n):
            x_j, y_j = coordinates[j]
            dx, dy = x_i - x_j, y_i - y_j
            d = int(round(math.hypot(dx, dy)))
            matrix[i][j] = matrix[j][i] = d
    return matrix

def cycle_cost(distance_matrix: List[List[int]], cycle: List[int]) -> int:
    cost = 0
    for i in range(len(cycle)-1):
        cost += distance_matrix[cycle[i]][cycle[i+1]]
    cost += distance_matrix[cycle[-1]][cycle[0]]
    return cost

def cycles_cost(distance_matrix: List[List[int]], cycle1: List[int], cycle2: List[int]) -> int:
    return cycle_cost(distance_matrix, cycle1) + cycle_cost(distance_matrix, cycle2)