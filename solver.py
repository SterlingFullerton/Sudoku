def printMatrix(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                print("_", end=" ")
            else:
                print(grid[i][j], end=" ")
        print()

def find_missing(grid):
    missing = False
    i = 0
    while missing == False and i < len(grid):
        j = 0
        while missing == False and j < len(grid[i]):
            if grid[i][j] == 0:
                missing = (i,j)
            j += 1
        i += 1
    return missing

def find_nums_to_check(grid, pos):
    nums = [1,2,3,4,5,6,7,8,9]
    row = pos[0]
    col = pos[1]

    #Check row
    for i in grid[row]:
        if i in nums:
            nums.remove(i)
    #Check col
    for i in range(9):
        if grid[i][col] in nums:
            nums.remove(grid[i][col])

    #group 9 rows into 3 big rows
    row = (row//3)*3
    col = (col//3)*3

    #Check sub-grid
    for i in range(row, row+3):
        for j in range(col, col+3):
            if grid[i][j] in nums:
                nums.remove(grid[i][j])

    return nums

def valid_grid(grid):
    #check rows
    for row in range(9):
        row_check = []
        for i in grid[row]:
            if i != 0 and i not in row_check:
                row_check.append(i)
            elif i != 0:
                return False

    #check cols
    for col in range(9):
        row_check = []
        for row in range(9):
            if grid[row][col] != 0 and grid[row][col] not in row_check:
                row_check.append(grid[row][col])
            elif grid[row][col] != 0:
                print('break 2')
                return False

    #check subgrids
    for subRow in range(0,9,3):
        for subCol in range(0,9,3):
            subgrid_check = []
            for row in range(subRow, subRow+3):
                for col in range(subCol, subCol+3):
                    num = grid[row][col]
                    if num != 0:
                        if num not in subgrid_check:
                            subgrid_check.append(num)
                        else:
                            return False

    return True

def solve(grid):
    pos = find_missing(grid)
    if pos != False:
        #Gather Possible Numbers for pos (x,y)
        nums_to_check = find_nums_to_check(grid, pos)
        #Check Possible Numbers
        for check_num in nums_to_check:
            #Check Num
            grid[pos[0]][pos[1]] = check_num
            #Recursive Solve
            solved = solve(grid)
            if solved == True:
                #Break Resursion if solved
                return True
            else:
                #Remove Digit if it didnt work
                grid[pos[0]][pos[1]] = 0
        return False
    else:
        #If pos not set, there are no more numbers to be tried.
        return True

grid=[[3,0,6,5,0,8,4,0,0],
      [5,2,0,0,0,0,0,0,0],
      [0,8,7,0,0,0,0,3,1],
      [0,0,3,0,1,0,0,8,0],
      [9,0,0,8,6,3,0,0,5],
      [0,5,0,0,9,0,6,0,0],
      [1,3,0,0,0,0,2,5,0],
      [0,0,0,0,0,0,0,7,4],
      [0,0,5,2,0,6,3,0,0]]

print("---Original Grid---")
printMatrix(grid)
if valid_grid(grid):
    print("\n---Valid Grid---\n")
    solve(grid)
    print("---Solved Grid---")
    printMatrix(grid)
else:
    print("Invalid Grid. Not attempting to solve")
