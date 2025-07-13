import os
from typing import List, Tuple

from matplotlib.axes import Axes
import matplotlib.pyplot as plt


def plot_solution(ax : Axes, cycle1 : List[int], cycle2 : List[int], coords : List[Tuple[float, float]], title : str) -> None:
    x1 = [coords[node][0] for node in cycle1]
    y1 = [coords[node][1] for node in cycle1]
    x1.append(x1[0])
    y1.append(y1[0])
    ax.plot(x1, y1, linewidth=1, marker="o", markersize=3)

    x2 = [coords[node][0] for node in cycle2]
    y2 = [coords[node][1] for node in cycle2]
    x2.append(x2[0])
    y2.append(y2[0])
    ax.plot(x2, y2, linewidth=1, marker="o", markersize=3)

    ax.set_title(title)
    ax.set_aspect("equal")
    ax.grid(True)


def plot_solutions(tsp_file : str, coords : List[Tuple[float, float]], solution : Tuple[List[int], List[int]], cost : float, show : bool = False)  -> None:
    output_dir = "charts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    basename = os.path.basename(tsp_file).replace(".tsp", "")
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_solution(
        ax,
        solution[0],
        solution[1],
        coords,
        f"Solution for {basename}\nCost: {cost:.2f}",
    )

    out_path = os.path.join(output_dir, f"{basename}.png")
    plt.savefig(out_path, dpi=300)
    if show:
        plt.show()
    else:
        plt.close()