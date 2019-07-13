# used Python2
# for Python3: 
#    1) Tkinter -> tkinter 
#    2) import tkFont -> from tkinter import font
#    3) tkFont -> font
#    4) small differences in window sizes

from Tkinter import Tk, Button, Label, Menu, Toplevel, Canvas, IntVar
import tkFont # for creation new font (underlined)
import webbrowser # for open GitHub
import Model
import time
import sys # for definition OS

# main-window
window = Tk()
window.resizable(False, False)
window.wm_geometry("+%d+%d" % 
                   ((window.winfo_screenwidth() - window.winfo_reqwidth()) / 3, 
                    (window.winfo_screenheight() - window.winfo_reqheight()) / 3))

buttonRestart = Button(window, text = "Restart")
labelGameOver = Label(window, font=("", 20))
labelNumberOfFlags = Label(window, font=("", 20))

# remember time of open first square
global timeStart

# about-window  
def aboutApp():
    # creation about-window if there is not (85 = 9x9 + 4; 260 = 16x16 + 4; 484 = 16x32 + 4)
    if window.winfo_children().__len__() in (85, 260, 484):
        aboutWindow = Toplevel(window)
        aboutWindow.title("About Minesweeper")
        aboutWindow.geometry("270x125")
        aboutWindow.resizable(False, False)
        aboutWindow.wm_geometry("+%d+%d" % 
                                  ((aboutWindow.winfo_screenwidth() / 2 - aboutWindow.winfo_reqwidth()), 
                                   (aboutWindow.winfo_screenheight() / 2 - aboutWindow.winfo_reqheight())))
        
        _ = Label(aboutWindow, text = "Minesweeper by Andrew Jeus", font=("", 18)).grid(row = 0, column = 0, padx = 10, pady = 10)
        _ = Label(aboutWindow, text = "Version 1.0 (12 July 2019)", font=("", 18)).grid(row = 1, column = 0)
        labelInfo3 = Label(aboutWindow, text = "View code in GitHub", font=("", 14))
        labelInfo3.grid(row = 2, column = 0, padx = 5, pady = 5)
        
        # my font for link to GitHub
        myfont = tkFont.Font(labelInfo3, labelInfo3.cget("font"))
        myfont.configure(underline = True)
        labelInfo3.configure(font = myfont)
        
        labelInfo3.bind("<Button-1>", lambda _: webbrowser.open_new("https://github.com/MickeyMouseMouse/Minesweeper"))

# settings menu bar (1 part)    
menubar = Menu()
window.config(menu = menubar)

fileMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "File", menu = fileMenu)
fileMenu.add_command(label = "About Minesweeper", command = aboutApp)
fileMenu.add_separator()
fileMenu.add_command(label = "Exit", command = exit)

# coordinates for print squares, flags, mines, numbers in different modes
easyModeSettings = [45, 16, 40, 24, 40, 20, 40, 20, 23, 19, 25, 19, 4, 34, 14, 9, 9, 35, 35, 22, 40, 22, 5, 4, 22, 40, 22, 22, 22, 25]
mediumAndHardModeSettings = [25, 9, 22, 13, 22, 11, 22, 11, 13, 10, 14, 10, 2, 19, 8, 5, 5, 19, 19, 12, 22, 12, 3, 2, 12, 22, 12, 12, 12, 15]
currentModeSettings = []

# flag for generation field (no defeat in first move)
firstMove = True

def restart(row = None, column = None): 
    Model.restart(row, column)
    
    global firstMove, currentModeSettings
    
    # cleaning GUI field for restart game on the same mode
    if not firstMove:
        listOfCanvas = window.grid_slaves() 
        for i in range(Model.x):
            for j in range(Model.y):
                c = listOfCanvas[Model.y * i + j]
                c.delete("all")
                c.create_rectangle(0, 0, currentModeSettings[0], currentModeSettings[0], fill = 'dark grey', outline = 'black', width = 1)
                
        firstMove = True        
            
    labelGameOver.config(text = "")     
    labelNumberOfFlags.config(text = Model.amountMines.__str__())
    
# event on press button Restart
buttonRestart.bind("<Button-1>", restart)   

# repaint squares in field  from list Minesweeper.repaintSquares
def repaintField():
    listOfCanvas = window.grid_slaves() 
    for coor in Model.repaintSquares:
        c = listOfCanvas[Model.y * coor.row + coor.column]
        c.delete("all")
        
        # paint flag
        if Model.field[coor.row][coor.column].conditionOfSquare == -1:
            c.create_rectangle(0, 0, currentModeSettings[0], currentModeSettings[0], fill = 'dark grey', outline = 'black', width = 1)
            c.create_line(currentModeSettings[1], currentModeSettings[2], currentModeSettings[3], currentModeSettings[4], width = 3) # horizontal leg
            c.create_line(currentModeSettings[5], currentModeSettings[6], currentModeSettings[7], currentModeSettings[8], width = 3) # vertical leg
            c.create_polygon(currentModeSettings[9], currentModeSettings[10], currentModeSettings[11], currentModeSettings[12], currentModeSettings[13], currentModeSettings[14], fill = "red", width = 3) # triangle
        
        # paint close square
        if Model.field[coor.row][coor.column].conditionOfSquare == 0:
            c.create_rectangle(0, 0, currentModeSettings[0], currentModeSettings[0], fill = 'dark grey', outline = 'black', width = 1)
        
        if Model.field[coor.row][coor.column].conditionOfSquare == 1:
            mines = Model.field[coor.row][coor.column].numberOfMines
            # paint mine
            if mines == -1:
                c.create_rectangle(0, 0, currentModeSettings[0], currentModeSettings[0], fill = 'red', outline = 'black', width = 1)
                c.create_oval(currentModeSettings[15], currentModeSettings[16], currentModeSettings[17], currentModeSettings[18], fill = "black")
                c.create_line(currentModeSettings[19], currentModeSettings[20], currentModeSettings[21], currentModeSettings[22], width = 3, fill = "black")
                c.create_line(currentModeSettings[23], currentModeSettings[24], currentModeSettings[25], currentModeSettings[26], width = 3, fill = "black")
            else:
                # paint open square with number
                c.create_rectangle(0, 0, currentModeSettings[0], currentModeSettings[0], fill = 'light grey', outline = 'black', width = 1)
                if mines != 0:
                    c.create_text(currentModeSettings[27], currentModeSettings[28], text = mines.__str__(), font=("", currentModeSettings[29]))        

# make next step
def step(row, column):
    global timeStart
    
    if not Model.gameOver: 
        result =  Model.makeNextMove(row, column)

        if result == -1:
            Model.openAllMines()
            labelGameOver.config(text = "Defeat", fg = "red")
            
        if result == 1:
            Model.setAllFlags()
            labelGameOver.config(text = "Win: " + (int(time.time() - timeStart)).__str__() + " s", fg = "green")   

        repaintField()

# set/unset flag
def flag(row, column):    
    if not Model.gameOver: 
        Model.setUnsetFlag(row, column)
        repaintField()
        labelNumberOfFlags.config(text = Model.numberOfFlags.__str__())   

# mouse event (left button)
def mouseButton1(_, row, column):
    global firstMove, timeStart
    
    if firstMove:
        restart(row, column) # (row, column) - first move should be without mine
        firstMove = False
        timeStart = time.time() 
    
    step(row, column)

# mouse event (right button)   
def mouseButton3(_, row, column):
    global firstMove
    
    if not firstMove:
        flag(row, column)  

# destroy old GUI field when select new mode
def destroyGUIField():
    listOfCanvas = window.grid_slaves() 
    for i in range(Model.x):
        for j in range(Model.y):
            listOfCanvas[Model.y * i + j].destroy()

# creation new GUI field        
def createGUIField():
    for i in range(Model.x, 0, -1):
        for j in range(Model.y - 1, -1, -1):
            c = Canvas(window, width = currentModeSettings[0], height = currentModeSettings[0], highlightthickness = 0)
            c.create_rectangle(0, 0, currentModeSettings[0], currentModeSettings[0], fill = 'dark grey', outline = 'black', width = 1)
            
            c.bind("<Button-1>", lambda event, row = i - 1, column = j: mouseButton1(event, row, column))
            if sys.platform in ("win32", "win64"):
                # windows: right mouse button = Button3
                c.bind("<Button-3>", lambda event, row = i - 1, column = j: mouseButton3(event, row, column))
            else:
                # macOs: right mouse button = Button2    
                c.bind("<Button-2>", lambda event, row = i - 1, column = j: mouseButton3(event, row, column))
            
            c.grid(row = i, column = j)
            
    global firstMove
    firstMove = True
    
    labelGameOver.config(text = "")     
    labelNumberOfFlags.config(text = Model.amountMines.__str__())    

# 1 = easy (9x9, 10)
# 2 = medium (16x16, 40)
# 3 = hard (16x30, 99)
mode = IntVar()
mode.set(1)
    
def setEasyMode():
    global mode, currentModeSettings, easyModeSettings
        
    destroyGUIField()
    
    Model.x = 9 
    Model.y = 9
    Model.amountMines = 10
    
    labelNumberOfFlags.grid(row = 0, column = 1, columnspan = 1)

    buttonRestart.grid(row = 0, column = 3, columnspan = 3, pady = 5)
    
    labelGameOver.grid(row = 0, column = 6, columnspan = 3)
    
    window.geometry("405x443")
    window.title("Minesweeper (9x9, 10 mine)")
    
    currentModeSettings = easyModeSettings
    createGUIField()
    Model.createField()

def setMediumMode():
    global mode, currentModeSettings, mediumAndHardModeSettings
       
    destroyGUIField()
    
    Model.x = 16 
    Model.y = 16
    Model.amountMines = 40

    labelNumberOfFlags.grid(row = 0, column = 1, columnspan = 2)
    
    buttonRestart.grid(row = 0, column = 6, columnspan = 4, pady = 5)
    
    labelGameOver.grid(row = 0, column = 11, columnspan = 5)        
    
    window.geometry("400x438")
    window.title("Minesweeper (16x16, 40 mine)")
    
    currentModeSettings = mediumAndHardModeSettings
    createGUIField()
    Model.createField()

def setHardMode():
    global mode, currentModeSettings, mediumAndHardModeSettings
        
    destroyGUIField()
    
    Model.x = 16 
    Model.y = 30
    Model.amountMines = 99
    
    labelNumberOfFlags.grid(row = 0, column = 1, columnspan = 2)
    
    buttonRestart.grid(row = 0, column = 13, columnspan = 4, pady = 5)
    
    labelGameOver.grid(row = 0, column = 25, columnspan = 4) 
    
    window.geometry("750x438")
    window.title("Minesweeper (16x30, 99 mine)")
    
    currentModeSettings = mediumAndHardModeSettings
    createGUIField()
    Model.createField()

# !!! START THE GAME !!!
setEasyMode()

# settings menu bar (2 part)                                    
gameModeMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Game mode", menu = gameModeMenu)
gameModeMenu.add_radiobutton(label = "Easy", command = setEasyMode, variable = mode, value = 1)
gameModeMenu.add_radiobutton(label = "Medium", command = setMediumMode, variable = mode, value = 2)
gameModeMenu.add_radiobutton(label = "Hard", command = setHardMode, variable = mode, value = 3)

window.mainloop()

         
    
                  
    
 
    
 
 
