# Sudoku Generator Algorithm - Paciurcă Andrei-Alexandru (http://andreipaciurca.github.io)
from random import randint, shuffle

# Initialise empty 9 by 9 grid
# grid = [[0 for col in range(9)] for row in range(9)]
grid = [grid[:] for grid in [[0] * 9] * 9]

# A function that prints in a 'nice' way a 2d-array
def printGrid(grid):
    print('\n'.join(['  '.join([str(cell) for cell in row]) for row in grid]))

# A function to check if the grid is full
def checkGrid(grid):
    for row in range(0,9):
                if 0 in grid[row]:
                    return False
    # We have a complete grid!
    return True

# A function that returns the current Box/Block/Nonet (3x3 matrix)
def getCurrentBox(grid,row,col):
        if row<3:
                if col<3:
                        return [grid[i][0:3] for i in range(0,3)]
                elif col<6:
                        return [grid[i][3:6] for i in range(0,3)]
                else:
                        return [grid[i][6:9] for i in range(0,3)]
        elif row<6:
                if col<3:
                        return [grid[i][0:3] for i in range(3,6)]
                elif col<6:
                        return [grid[i][3:6] for i in range(3,6)]
                else:
                        return [grid[i][6:9] for i in range(3,6)]
        else:
                if col<3:
                        return [grid[i][0:3] for i in range(6,9)]
                elif col<6:
                        return [grid[i][3:6] for i in range(6,9)]
                else:
                        return [grid[i][6:9] for i in range(6,9)]

# A backtracking/recursive function to check all possible combinations of numbers until a solution is found
def solveGrid(grid):
    global counter
    # Find next empty cell
    for i in range(0,81):
        row=i//9
        col=i%9
        if grid[row][col] == 0:
            for value in range (1,10):
                # Check that this value has not already be used on this row
                if not(value in grid[row]):
                    # Check that this value has not already be used on this column
                    if not value in list(val[col] for val in grid):
                        # Identify which of the 9 squares we are working on
                        square=getCurrentBox(grid,row,col)
                        # Check that this value has not already be used on this 3x3 square
                        if not value in (square[0] + square[1] + square[2]):
                            grid[row][col] = value
                            if checkGrid(grid):
                                counter += 1
                                break
                            else:
                                if solveGrid(grid):
                                    return True
            break
    grid[row][col] = 0

# A numberList = [1,2,...,9] that will be randomized using shuffle() function from random
numberList = list(range(1,10))

# A backtracking/recursive function to check all possible combinations of numbers until a solution is found
def fillGrid(grid):
    global counter
    # Find next empty cell
    for i in range(0,81):
        row = i//9
        col = i%9
        if grid[row][col] == 0:
            shuffle(numberList)
            for value in numberList:
                # Check that this value has not already be used on this row
                if not(value in grid[row]):
                    # Check that this value has not already be used on this column
                     if not value in list(val[col] for val in grid):
                        # Identify which of the 9 squares we are working on
                        square=getCurrentBox(grid,row,col)
                        # Check that this value has not already be used on this 3x3 square
                        if not value in (square[0] + square[1] + square[2]):
                            grid[row][col] = value
                            if checkGrid(grid):
                                return True
                            else:
                                if fillGrid(grid):
                                    return True
            break
    grid[row][col] = 0

# Generate a Fully Solved Grid
fillGrid(grid)
printGrid(grid)

# Start Removing Numbers one by one
# A higher number of attempts will end up removing more numbers from the grid
# Potentially resulting in more difficiult grids to solve!
attempts = 3
counter = 1
while attempts>0:
    # Select a random cell that is not already empty
    row = randint(0,8)
    col = randint(0,8)
    while grid[row][col] == 0:
        row = randint(0,8)
        col = randint(0,8)
    # Remember its cell value in case we need to put it back
    backup = grid[row][col]
    grid[row][col] = 0

    # Take a full copy of the grid
    # grig[:] instead of plain grid to make sure that the copy does not reffer to the same memory location
    copyGrid = grid[:]

    # Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
    counter = 0
    solveGrid(copyGrid)
    # If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
    if counter != 1:
        grid[row][col] = backup
        # We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
        attempts -= 1

print("\n Sudoku Grid Ready: \n")
printGrid(grid)
