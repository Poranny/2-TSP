[![CI](https://github.com/Poranny/2-TSP/actions/workflows/ci.yml/badge.svg)](https://github.com/Poranny/Sssnake/actions) [![codecov](https://codecov.io/gh/Poranny/Two-TSP/graph/badge.svg?token=W1WXPE0X2H)](https://codecov.io/gh/Poranny/Two-TSP) ![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)

# 2-TSP solver

A comprehensive Python implementation of heuristic algorithms for the 2-cycle Traveling Salesman Problem (2-TSP), encompassing:
- constructive methods (greedy and regret-based cycle algorithms),
- local search heuristics (vertex and edge-based steepest descent, candidate moves, move-list strategies),
- advanced metaheuristics (Multi-Start Local Search, Iterated Local Search, Large Neighborhood Search),
- as well as a hybrid evolutionary algorithm with mutations.

Core features are verified using rudimentary pytest tests.
Simple solution visualization using matplotlib is also included.
#### Sample plot for kroA100 - HAE + LS
<img src="two_tsp/utils/charts/kroA100.png" alt="Plot for kroA100 - HAE + LS" width="400"/>
