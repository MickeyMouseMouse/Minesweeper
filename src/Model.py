import random

class Square:
    numberOfMines = 0 # -1 = mine, 0..n = number of mines
    conditionOfSquare = 0 # -1 = flag, 0 = close (without flag), 1 = open
    
class CoordinatesOfSquare:
    def __init__(self, i, j):
        self.row = i
        self.column = j   

# number of free flags
global numberOfFlags

global numberOfOpendSquares

# flag for end the game
global gameOver

# matrix of game field
global field

# size of field
x = 0 # 0 = !default! value after start the app
y = 0 # 0 = !default! value after start the app

# number of mines in the current mode
global amountMines

# need to open 'openForWin' squares to win
global openForWin

# stores the coordinates of the squares for repaint
global repaintSquares

# create field
def createField():       
    global field 
    field = []
    
    for _ in range(x):
        tmp = []
        for _ in range(y):
            tmp.append(Square())
        field.append(tmp)    

def restart(firstRow, firstColumn):
    global numberOfFlags, numberOfOpendSquares, gameOver, openForWin
    
    numberOfFlags = amountMines
    numberOfOpendSquares = 0
    gameOver = False
    openForWin = x * y - amountMines
    
    # default values for field
    for i in range(x):
        for j in range(y):
            field[i][j].numberOfMines = 0
            field[i][j].conditionOfSquare = 0
    
    # installation of 10 mines in a random order
    i = 0
    while i < amountMines:
        row = random.randrange(0, x, 1)
        column = random.randrange(0, y, 1)
        
        if (row == firstRow and column == firstColumn): continue
        
        if field[row][column].numberOfMines == 0:
            field[row][column].numberOfMines = -1
            i += 1
        else:
            continue    

    # calculating number of mines for all empty squares
    for i in range(x):
        for j in range(y):
            if field[i][j].numberOfMines == -1: continue
            
            number = 0
            if i - 1 != -1 and j - 1 != -1:
                if field[i - 1][j - 1].numberOfMines == -1: number += 1
            if i - 1 != -1:
                if field[i - 1][j].numberOfMines == -1: number += 1
            if i - 1 != -1 and j + 1 != y:
                if field[i - 1][j + 1].numberOfMines == -1: number += 1
            if j - 1 != -1:
                if field[i][j - 1].numberOfMines == -1: number += 1
            if j + 1 != y:
                if field[i][j + 1].numberOfMines == -1: number += 1
            if i + 1 != x and j - 1 != -1:
                if field[i + 1][j - 1].numberOfMines == -1: number += 1
            if i + 1 != x:
                if field[i + 1][j].numberOfMines == -1: number += 1
            if i + 1 != x and j + 1 != y:
                if field[i + 1][j + 1].numberOfMines == -1: number += 1
                
            field[i][j].numberOfMines = number   

# set/unset flags        
def setUnsetFlag(row, column):
    global numberOfFlags, repaintSquares
    
    repaintSquares = []
    
    if field[row][column].conditionOfSquare == -1:
        field[row][column].conditionOfSquare = 0
        numberOfFlags += 1
        repaintSquares.append(CoordinatesOfSquare(row, column))
    else:    
        if field[row][column].conditionOfSquare == 0:
            if numberOfFlags > 0:
                field[row][column].conditionOfSquare = -1
                numberOfFlags -= 1
                repaintSquares.append(CoordinatesOfSquare(row, column))

# make next move;
# return -1 if Mine (game over)
# returns 0 if Ok  
# returns 1 if win
def makeNextMove(row, column):
    global numberOfOpendSquares, gameOver, repaintSquares

    repaintSquares = []
    
    if field[row][column].conditionOfSquare == 0:
        field[row][column].conditionOfSquare = 1 # open square
        numberOfOpendSquares += 1
        repaintSquares.append(CoordinatesOfSquare(row, column))
        
        if field[row][column].numberOfMines == -1: 
            gameOver = True
            return -1 # Mine => game over
        
        if field[row][column].numberOfMines == 0:
            checkZeroSquares(row, column)    
        
        if numberOfOpendSquares == openForWin:
            gameOver = True
            return 1 # win
        else:
            return 0 # Ok

def checkZeroSquares(row, column):
    global numberOfOpendSquares, repaintSquares

    i = row - 1
    j = column - 1
    while (i != -1 and j != -1 and field[i][j].numberOfMines != -1
           and field[i][j].conditionOfSquare == 0):
        field[i][j].conditionOfSquare = 1
        numberOfOpendSquares += 1
        repaintSquares.append(CoordinatesOfSquare(i, j))
        
        if field[i][j].numberOfMines == 0: checkZeroSquares(i, j)
        
    i = row - 1
    j = column
    while (i != -1 and field[i][j].numberOfMines != -1
           and field[i][j].conditionOfSquare == 0):
        field[i][j].conditionOfSquare = 1
        numberOfOpendSquares += 1
        repaintSquares.append(CoordinatesOfSquare(i, j))
        
        if field[i][j].numberOfMines == 0: checkZeroSquares(i, j)
                
    i = row - 1
    j = column + 1
    while (i != -1 and j != y and field[i][j].numberOfMines != -1
           and field[i][j].conditionOfSquare == 0):
        field[i][j].conditionOfSquare = 1
        numberOfOpendSquares += 1
        repaintSquares.append(CoordinatesOfSquare(i, j))
        
        if field[i][j].numberOfMines == 0: checkZeroSquares(i, j)
    
    i = row
    j = column - 1
    while (j != -1 and field[i][j].numberOfMines != -1
           and field[i][j].conditionOfSquare == 0):
        field[i][j].conditionOfSquare = 1
        numberOfOpendSquares += 1
        repaintSquares.append(CoordinatesOfSquare(i, j))
        
        if field[i][j].numberOfMines == 0: checkZeroSquares(i, j)
     
    i = row
    j = column + 1
    while (j != y and field[i][j].numberOfMines != -1
           and field[i][j].conditionOfSquare == 0):
        field[i][j].conditionOfSquare = 1
        numberOfOpendSquares += 1
        repaintSquares.append(CoordinatesOfSquare(i, j))
        
        if field[i][j].numberOfMines == 0: checkZeroSquares(i, j)
     
    i = row + 1
    j = column - 1
    while (i != x and j != -1 and field[i][j].numberOfMines != -1
           and field[i][j].conditionOfSquare == 0):
        field[i][j].conditionOfSquare = 1
        numberOfOpendSquares += 1
        repaintSquares.append(CoordinatesOfSquare(i, j))
        
        if field[i][j].numberOfMines == 0: checkZeroSquares(i, j)
                
    i = row + 1
    j = column
    while (i != x and field[i][j].numberOfMines != -1
           and field[i][j].conditionOfSquare == 0):
        field[i][j].conditionOfSquare = 1
        numberOfOpendSquares += 1
        repaintSquares.append(CoordinatesOfSquare(i, j))
        
        if field[i][j].numberOfMines == 0: checkZeroSquares(i, j)

    i = row + 1
    j = column + 1
    while (i != x and j != y and field[i][j].numberOfMines != -1
           and field[i][j].conditionOfSquare == 0):
        field[i][j].conditionOfSquare = 1
        numberOfOpendSquares += 1
        repaintSquares.append(CoordinatesOfSquare(i, j))
        
        if field[i][j].numberOfMines == 0: checkZeroSquares(i, j)

# open every mine       
def openAllMines():
    for i in range(x):
        for j in range(y):
            if field[i][j].numberOfMines == -1:
                field[i][j].conditionOfSquare = 1
                repaintSquares.append(CoordinatesOfSquare(i, j))

# set flag on every mine                
def setAllFlags():
    for i in range(x):
        for j in range(y):
            if field[i][j].numberOfMines == -1:
                if field[i][j].conditionOfSquare != -1:
                    field[i][j].conditionOfSquare = -1    
                    repaintSquares.append(CoordinatesOfSquare(i, j))                             