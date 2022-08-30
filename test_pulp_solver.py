import pulp_solver



CAGE_CONSTRAINTS = [
    (3, [[0, 0], [0, 1]]),
    (15, [[0, 2], [0, 3], [0, 4]]),
    (22, [[0, 5], [1, 5], [1, 4], [2, 4]]),
    (4, [[0, 6], [1, 6]]),
    (16, [[0, 7], [1, 7]]),
    (15, [[0, 8], [1, 8], [2, 8], [3, 8]]),
    (25, [[1, 0], [1, 1], [2, 0], [2, 1]]),
    (17, [[1, 2], [1, 3]]),
    (9, [[2, 2], [2, 3], [3, 3]]),
    (8, [[2, 5], [3, 5], [4, 5]]),
    (20, [[2, 6], [2, 7], [3, 6]]),
    (6, [[3, 0], [4, 0]]),
    (14, [[3, 1], [3, 2]]),
    (17, [[3, 4], [4, 4], [5, 4]]),
    (17, [[3, 7], [4, 7], [4, 6]]),
    (13, [[4, 1], [4, 2], [5, 1]]),
    (20, [[4, 3], [5, 3], [6, 3]]),
    (12, [[4, 8], [5, 8]]),
    (27, [[5, 0], [6, 0], [7, 0], [8, 0]]),
    (6, [[5, 2], [6, 2], [6, 1]]),
    (20, [[5, 5], [6, 5], [6, 6]]),
    (6, [[5, 6], [5, 7]]),
    (10, [[6, 4], [7, 4], [7, 3], [8, 3]]),
    (14, [[6, 7], [6, 8], [7, 7], [7, 8]]),
    (8, [[7, 1], [8, 1]]),
    (16, [[7, 2], [8, 2]]),
    (15, [[7, 5], [7, 6]]),
    (13, [[8, 4], [8, 5], [8, 6]]),
    (17, [[8, 7], [8, 8]])
]


def test_solve():
    killer_solver = pulp_solver.KillerSudokuSolver(cagesList=CAGE_CONSTRAINTS)

    solution = killer_solver.solve()

    for row in solution:
        print(row)


def main():
    test_solve()


if __name__ == '__main__':
    main()
