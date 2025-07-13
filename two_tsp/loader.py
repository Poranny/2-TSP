import tsplib95
from typing import List, Tuple

def load_instance(file_name: str) -> List[Tuple[float, float]]:
    problem = tsplib95.load(file_name)
    return [coord for _, coord in sorted(problem.node_coords.items())]
