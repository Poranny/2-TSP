from typing import List, Tuple, Set

from two_tsp.helpers import (
    delta_2opt,
    delta_between,
    check_all_edges,
    apply_2opt,
    check_all_edges_two_cycles,
    apply_between,
    find_nearest_neighbors,
)

Edge = Tuple[int, int]
Move = Tuple[float, str, Tuple[int, int], List[Edge], List[Edge]]


def local_search_with_move_list(
    cycle1: List[int], cycle2: List[int], distance_matrix: List[List[float]]
) -> Tuple[List[int], List[int]]:
    c1: List[int] = cycle1[:]
    c2: List[int] = cycle2[:]

    move_list: List[Move] = []

    n1 = len(c1)

    for i in range(n1):
        for j in range(i + 2, n1):
            if (j + 1) % n1 == i:
                continue
            d = delta_2opt(distance_matrix, c1, i, j)
            if d < 0:
                edges_removed = [(c1[i], c1[(i + 1) % n1]), (c1[j], c1[(j + 1) % n1])]
                move_list.append((d, "2opt1", (i, j), edges_removed, []))

    n2 = len(c2)

    for i in range(n2):
        for j in range(i + 2, n2):
            if (j + 1) % n2 == i:
                continue
            d = delta_2opt(distance_matrix, c2, i, j)
            if d < 0:
                edges_removed = [(c2[i], c2[(i + 1) % n2]), (c2[j], c2[(j + 1) % n2])]
                move_list.append((d, "2opt2", (i, j), edges_removed, []))

    for i in range(n1):
        for j in range(n2):
            d = delta_between(distance_matrix, c1, c2, i, j)
            if d < 0:
                i_prev = (i - 1) % n1
                i_next = (i + 1) % n1
                j_prev = (j - 1) % n2
                j_next = (j + 1) % n2

                edges_removed_c1 = [(c1[i_prev], c1[i]), (c1[i], c1[i_next])]
                edges_removed_c2 = [(c2[j_prev], c2[j]), (c2[j], c2[j_next])]

                move_list.append(
                    (d, "swap", (i, j), edges_removed_c1, edges_removed_c2)
                )

    move_list.sort(key=lambda x: x[0])

    while move_list:
        delta, move_type, (i, j), edges_c1, edges_c2 = move_list.pop(0)
        new_move_list :List[Move] = []
        if move_type == "2opt1":
            status = check_all_edges(c1, edges_c1)
            if status == 0:
                continue
            elif status == 1:
                move_list.append((delta, move_type, (i, j), edges_c1, edges_c2))
                continue
            else:
                c1 = apply_2opt(c1, i, j)

                new_move_list = []
                for m in move_list:
                    d_m, t_m, (i_m, j_m), e1_m, e2_m = m
                    if t_m == "2opt1":
                        if (
                            i <= i_m <= j
                            or i <= j_m <= j
                            or i_m <= i <= j_m
                            or i_m <= j <= j_m
                        ):
                            continue
                    elif t_m == "swap":
                        st = check_all_edges_two_cycles(c1, c2, e1_m, e2_m)
                        if st == 0:
                            continue
                    new_move_list.append(m)
                move_list = new_move_list

                n1 = len(c1)
                for ni in range(n1):
                    for nj in range(ni + 2, n1):
                        if (nj + 1) % n1 == ni:
                            continue
                        d_new = delta_2opt(distance_matrix, c1, ni, nj)
                        if d_new < 0:
                            erem = [
                                (c1[ni], c1[(ni + 1) % n1]),
                                (c1[nj], c1[(nj + 1) % n1]),
                            ]
                            move_list.append((d_new, "2opt1", (ni, nj), erem, []))

                n2 = len(c2)
                for ni in range(n1):
                    for nj in range(n2):
                        d_new = delta_between(distance_matrix, c1, c2, ni, nj)
                        if d_new < 0:
                            i_prev = (ni - 1) % n1
                            i_next = (ni + 1) % n1
                            j_prev = (nj - 1) % n2
                            j_next = (nj + 1) % n2

                            e_c1 = [(c1[i_prev], c1[ni]), (c1[ni], c1[i_next])]
                            e_c2 = [(c2[j_prev], c2[nj]), (c2[nj], c2[j_next])]
                            move_list.append((d_new, "swap", (ni, nj), e_c1, e_c2))

                move_list.sort(key=lambda x: x[0])
                continue

        elif move_type == "2opt2":
            status = check_all_edges(c2, edges_c1)
            if status == 0:
                continue
            elif status == 1:
                move_list.append((delta, move_type, (i, j), edges_c1, edges_c2))
                continue
            else:
                c2 = apply_2opt(c2, i, j)
                new_move_list = []
                for m in move_list:
                    d_m, t_m, (i_m, j_m), e1_m, e2_m = m
                    if t_m == "2opt2":
                        if (
                            i <= i_m <= j
                            or i <= j_m <= j
                            or i_m <= i <= j_m
                            or i_m <= j <= j_m
                        ):
                            continue
                    elif t_m == "swap":
                        st = check_all_edges_two_cycles(c1, c2, e1_m, e2_m)
                        if st == 0:
                            continue
                    new_move_list.append(m)
                move_list = new_move_list

                n2 = len(c2)
                for ni in range(n2):
                    for nj in range(ni + 2, n2):
                        if (nj + 1) % n2 == ni:
                            continue
                        d_new = delta_2opt(distance_matrix, c2, ni, nj)
                        if d_new < 0:
                            erem = [
                                (c2[ni], c2[(ni + 1) % n2]),
                                (c2[nj], c2[(nj + 1) % n2]),
                            ]
                            move_list.append((d_new, "2opt2", (ni, nj), erem, []))

                n1 = len(c1)
                for ni in range(n1):
                    for nj in range(n2):
                        d_new = delta_between(distance_matrix, c1, c2, ni, nj)
                        if d_new < 0:
                            i_prev = (ni - 1) % n1
                            i_next = (ni + 1) % n1
                            j_prev = (nj - 1) % n2
                            j_next = (nj + 1) % n2

                            e_c1 = [(c1[i_prev], c1[ni]), (c1[ni], c1[i_next])]
                            e_c2 = [(c2[j_prev], c2[nj]), (c2[nj], c2[j_next])]
                            move_list.append((d_new, "swap", (ni, nj), e_c1, e_c2))

                move_list.sort(key=lambda x: x[0])
                continue

        elif move_type == "swap":
            status = check_all_edges_two_cycles(c1, c2, edges_c1, edges_c2)

            if status == 0:
                continue

            elif status == 1:
                move_list.append((delta, move_type, (i, j), edges_c1, edges_c2))
                continue

            else:
                apply_between(c1, c2, i, j)
                new_move_list = []

                for d_m, t_m, (i_m, j_m), e1_m, e2_m in move_list:
                    if t_m == "2opt1":
                        st = check_all_edges(c1, e1_m)

                        if st == 0:
                            continue

                    elif t_m == "2opt2":
                        st = check_all_edges(c2, e1_m)

                        if st == 0:
                            continue

                    else:
                        st = check_all_edges_two_cycles(c1, c2, e1_m, e2_m)

                        if st == 0:
                            continue

                    new_move_list.append((d_m, t_m, (i_m, j_m), e1_m, e2_m))

                move_list = new_move_list

                n1 = len(c1)
                neighborhood_c1: Set[int] = set()

                for offset in [-2, -1, 0, 1, 2]:
                    neighborhood_c1.add((i + offset) % n1)

                neigh_list = sorted(neighborhood_c1)
                k = len(neigh_list)

                for idx1 in range(k):
                    for idx2 in range(idx1 + 2, k):
                        ni = neigh_list[idx1]
                        nj = neigh_list[idx2]

                        if (nj + 1) % n1 == ni:
                            continue

                        d_new = delta_2opt(distance_matrix, c1, ni, nj)

                        if d_new < 0:
                            erem = [
                                (c1[ni], c1[(ni + 1) % n1]),
                                (c1[nj], c1[(nj + 1) % n1]),
                            ]

                            move_list.append((d_new, "2opt1", (ni, nj), erem, []))

                n2 = len(c2)
                neighborhood_c2: Set[int] = set()

                for offset in [-2, -1, 0, 1, 2]:
                    neighborhood_c2.add((j + offset) % n2)

                neigh_list2 = sorted(neighborhood_c2)
                k2 = len(neigh_list2)

                for idx1 in range(k2):
                    for idx2 in range(idx1 + 2, k2):
                        ni = neigh_list2[idx1]
                        nj = neigh_list2[idx2]

                        if (nj + 1) % n2 == ni:
                            continue

                        d_new = delta_2opt(distance_matrix, c2, ni, nj)

                        if d_new < 0:
                            erem = [
                                (c2[ni], c2[(ni + 1) % n2]),
                                (c2[nj], c2[(nj + 1) % n2]),
                            ]
                            move_list.append((d_new, "2opt2", (ni, nj), erem, []))

                for ni in neighborhood_c1:
                    for nj in neighborhood_c2:
                        d_new = delta_between(distance_matrix, c1, c2, ni, nj)
                        if d_new < 0:
                            i_prev = (ni - 1) % n1
                            i_next = (ni + 1) % n1
                            j_prev = (nj - 1) % n2
                            j_next = (nj + 1) % n2
                            e_c1 = [(c1[i_prev], c1[ni]), (c1[ni], c1[i_next])]

                            e_c2 = [(c2[j_prev], c2[nj]), (c2[nj], c2[j_next])]

                            move_list.append((d_new, "swap", (ni, nj), e_c1, e_c2))

                move_list.sort(key=lambda x: x[0])

                continue

    return c1, c2


def local_search_with_candidates(
    cycle1: List[int],
    cycle2: List[int],
    distance_matrix: List[List[float]],
    k: int = 10,
) -> Tuple[List[int], List[int]]:
    c1: List[int] = cycle1[:]
    c2: List[int] = cycle2[:]

    nearest_neighbors = find_nearest_neighbors(distance_matrix, k)

    improved = True
    while improved:
        improved = False
        best_delta = 0.0
        best_move: Tuple[int, int] | None = None
        best_type: str | None = None

        n1 = len(c1)
        for i in range(n1):
            i_next = (i + 1) % n1
            v_i = c1[i]
            v_i_next = c1[i_next]

            for j in range(i + 2, n1 - 1):
                j_next = (j + 1) % n1
                v_j = c1[j]
                v_j_next = c1[j_next]

                if (
                    v_j in nearest_neighbors[v_i]
                    or v_j_next in nearest_neighbors[v_i_next]
                    or v_i in nearest_neighbors[v_j]
                    or v_i_next in nearest_neighbors[v_j_next]
                ):
                    if (j + 1) % n1 == i:
                        continue

                    d = delta_2opt(distance_matrix, c1, i, j)
                    if d < best_delta:
                        best_delta = d
                        best_move = (i, j)
                        best_type = "2opt1"

        n2 = len(c2)
        for i in range(n2):
            i_next = (i + 1) % n2
            v_i = c2[i]
            v_i_next = c2[i_next]

            for j in range(i + 2, n2 - 1):
                j_next = (j + 1) % n2
                v_j = c2[j]
                v_j_next = c2[j_next]

                if (
                    v_j in nearest_neighbors[v_i]
                    or v_j_next in nearest_neighbors[v_i_next]
                    or v_i in nearest_neighbors[v_j]
                    or v_i_next in nearest_neighbors[v_j_next]
                ):
                    if (j + 1) % n2 == i:
                        continue

                    d = delta_2opt(distance_matrix, c2, i, j)
                    if d < best_delta:
                        best_delta = d
                        best_move = (i, j)
                        best_type = "2opt2"

        if best_delta < 0 and best_move and best_type:
            improved = True

            if best_type == "2opt1":
                i, j = best_move
                c1 = apply_2opt(c1, i, j)

            elif best_type == "2opt2":
                i, j = best_move
                c2 = apply_2opt(c2, i, j)
    return c1, c2
