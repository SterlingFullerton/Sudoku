#Imports and Inits
import pygame, sys, time
from pygame.locals import *

size = [273,400]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sudoku Solver")
pygame.init()
#Variable Creation

grid=[[3,0,6,5,0,8,4,0,0],
      [5,2,0,0,0,0,0,0,0],
      [0,8,7,0,0,0,0,3,1],
      [0,0,3,0,1,0,0,8,0],
      [9,0,0,8,6,3,0,0,5],
      [0,5,0,0,9,0,6,0,0],
      [1,3,0,0,0,0,2,5,0],
      [0,0,0,0,0,0,0,7,4],
      [0,0,5,2,0,6,3,0,0]]

#Colors
TRANSPARENT = pygame.Surface(size)
WHITE = (255,255,255)
GREY1 = (170,170,170)
GREY2 = (130,130,130)
GREY3 = (90,90,90)
BLACK = (0,0,0)

reg_font = pygame.font.SysFont("courier", 28, 1)


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
            drawNumbers(screen)
            drawGrid(screen)
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

def drawScreen(screen):
    screen.fill(WHITE)

def drawGrid(screen):
    for i in range(0,280,30):
        pygame.draw.rect(screen, GREY1, [0, i, 270, 3]) #Left, Top, Width, Height
        pygame.draw.rect(screen, GREY1, [i, 0, 3, 270]) # left base shade
    pygame.draw.rect(screen, GREY1, [270,270,3,3])

def drawNumbers(screen):
    x, y = 8,1
    for row in grid:
        for col in row:
            if col != 0:
                txt = reg_font.render(str(col), True, BLACK)
                pygame.draw.rect(screen, WHITE, [x,y,30,30])
                screen.blit(txt, (x,y))
            x += 30
        y += 30
        x = 8


drawScreen(screen)
drawNumbers(screen)
drawGrid(screen)

#Solve Button
solveTxt = reg_font.render("Solve", True, BLACK)
solveButton = pygame.draw.rect(screen, GREY1, [10,300,85,30])
screen.blit(solveTxt, (10, 300))

pygame.display.flip()


'''
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
'''


while True:
    pos = pygame.mouse.get_pos()
    mouse = pygame.draw.circle(TRANSPARENT, (0, 0, 0), pos , 0)
    #mouse = pygame.draw.circle(TRANSPARENT, (0, 0, 0), pos , 0)

    # Event Detection
    for event in pygame.event.get():
        print(event.type)
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if solveButton.contains(mouse):
                solve(grid)
            #pygame.draw(screen, (155, 155, 155), (pos, 5,5))
        pygame.display.flip()
