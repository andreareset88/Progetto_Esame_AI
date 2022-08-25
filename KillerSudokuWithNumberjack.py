from Numberjack import *
 
 
def defineModuleAnd SudokuGrid():
    N = 3
    cagesList = parseCages(examplecages)
 
    sudokuGrid = Matrix(N*N, N*N, 1, N*N)
 
    # Each row has to contain distinct 0-9 values and
    # each column has to contain distinct 0-9 values
    model = Model(
        [AllDiff(row) for row in sudokuGrid.row],
        [AllDiff(col) for col in sudokuGrid.col],
 
        # Each sub-matrix has to contain distinct 0-9 values
        [AllDiff(sudokuGrid[x:x + N, y:y + N]) for x in range(0, N*N, N)
            for y in range(0, N * N, N)],
    )
 
    # Contents of cages must be distinct.
    for totalValue, cellList in cagesList:
        cagecells = [sudokuGrid.flat[x] for x in cellList]
        model += AllDiff(cagecells)
        model += Sum(cagecells) == totalValue
 
    return sudokuGrid, model
 
 
def solve():
    sudokuGrid, model = defineModuleAnd SudokuGrid()
 
    solver = model.load('Mistral')
    solver.setVerbosity(0)
    solver.solve()
 
    if solver.is_sat():
        print(str(sudokuGrid))
    elif solver.is_unsat():
        print("Not satisfiable")
    else:
        print("Unknown")
 
 
def parseCagesList(textblob):
    cages = []
    for line in textblob.split("\n"):
        if not line.strip():
            continue
        bits = map(int, line.split())
        cages.append((bits[0], bits[1:]))
    return cages
 
 
examplecages = """
3 0 1
15 2 3 4
22 5 13 14 22
4 6 15
16 7 16
15 8 17 26 35
25 9 10 18 19
17 11 12
9 20 21 30
8 23 32 41
20 24 25 33
6 27 36
14 28 29
17 31 40 49
17 34 42 43
13 37 38 46
20 39 48 57
12 44 53
27 45 54 63 72
6 47 55 56
20 50 59 60
6 51 52
10 58 66 67 75
14 61 62 70 71
8 64 73
16 65 74
15 68 69
13 76 77 78
17 79 80
"""
 
 
if __name__ == '__main__':
    default = {'N': 3, 'solver': 'Mistral', 'verbose': 0}
    param = input(default)
    solve()