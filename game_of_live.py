import sys, math, random
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randint

speed = 300
cell_size = 20

class MouseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Mouse Tracker')
        self.label = QLabel(self)
        self.label.resize(200, 40)
        self.show()


class Drawing(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFocusPolicy( Qt.StrongFocus )

        self.brush = QBrush(QColor(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))        # set fillColor  
        self.pen = QPen(QColor(0,0,0,0))                      # set lineColor
        self.pen.setWidth(1)                                            # set lineWidth
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)

        pieceColor = {
            1:Qt.cyan, 
            2:Qt.yellow,
            3:Qt.darkMagenta,
            4:QColor("orange"),
            5:Qt.blue,
            6:Qt.red,
            7:Qt.green,
            8:QColor(0,50,100,50),
        }

        for w in range(0,game.width):
            for h in range(game.heigth):
                if game.board[w][h] >= 1:
                    if game.board[w][h] > 10:
                        self.brush = QColor(150,0,0,200)
                    else:
                        self.brush = QColor(0,0,100,150)
                else:
                    self.brush = QColor(0,0,100,0)
                self.pen = QPen(QColor(255,255,255,255))
                painter.setBrush(self.brush)
                painter.drawRect(w*cell_size,h*cell_size,cell_size,cell_size)

        if game.edit:
            self.brush = QColor(150,150,150,250)
            painter.setBrush(self.brush)
            painter.drawRect(game.cursor[0]*cell_size,game.cursor[1]*cell_size,cell_size,cell_size)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            game.stepToNextGen()
        if event.key() == Qt.Key_E:
            game.editMode()
        if event.key() == Qt.Key_Down:
            game.moveCursor("down")
        if event.key() == Qt.Key_Left:
            game.moveCursor("left")
        if event.key() == Qt.Key_Right:
            game.moveCursor("right")
        if event.key() == Qt.Key_Up:
            game.moveCursor("up")
        if event.key() == Qt.Key_Space:
            game.pause()
        if event.key() == Qt.Key_T:
            game.toggleCellUnderCursor() 
        if event.key() == Qt.Key_Escape:
            sys.exit(0)

        self.repaint() 

    def mouseMoveEvent(self, event):
        if game.edit:
            if game.cursor[0] != int(event.x()/cell_size) or game.cursor[1] != int(event.y()/cell_size):
                game.cursor[0] = int(event.x()/cell_size)
                game.cursor[1] = int(event.y()/cell_size)
                self.repaint()

    def mousePressEvent(self, QMouseEvent):
        if game.edit:
            game.toggleCellUnderCursor()

class GameController():
    def __init__(self,width,heigth):
        print('Create game ', width, 'x', heigth)

        self.width = width
        self.heigth = heigth

        self.running = True
        self.generation = 0

        self.edit = False
        self.cursor = [int(width/2), int(heigth/2)]

        self.board = []
        for w in range(width):
            self.board.append([])
            for h in range(heigth):
                self.board[w].append(random.randint(0,1))
        self.nextGen = []

        #self.board[4][4] = 1
        #self.board[4][5] = 1
        #self.board[4][6] = 1
  
        self.tick = QTimer()
        self.tick.timeout.connect(self.ticked)
        self.tick.start(speed)

    def editMode(self):
        if self.edit:
            self.pause()
            self.edit = False
        else:
            if self.running:
                self.pause()
                self.edit = True

        print("Edit mode: ", self.edit)

    def toggleCellUnderCursor(self):
        print("Toggle Cell at: ", self.cursor[0], ", ", self.cursor[1])

        if self.board[self.cursor[0]][self.cursor[1]] > 0:
            self.board[self.cursor[0]][self.cursor[1]] = 0
        else:
            self.board[self.cursor[0]][self.cursor[1]] = 1

    def moveCursor(self, direction):
        if direction == "up":
            self.cursor[1] -= 1
        if direction == "down":
            self.cursor[1] += 1
        if direction == "left":
            self.cursor[0] -= 1
        if direction == "right":
            self.cursor[0] += 1

        if self.cursor[0] < 0:
            self.cursor[0] = 0
        if self.cursor[0] > self.width:
            self.cursor[0] = self.width
        if self.cursor[1] < 0:
            self.cursor[1] = 0
        if self.cursor[1] > self.heigth:
            self.cursor[1] = self.heigth

    def pause(self):
        if self.running:
            self.tick.stop()
            self.running = False
            print('Stop')
        else:
            self.tick.start(speed)
            self.running = True
            print('Continue')

    def stepToNextGen(self):
        print('Step to next generation')
        if self.running:
            self.tick.stop()
            self.tick.singleShot(speed,self.ticked)
            self.running = False
        else:
            self.tick.singleShot(speed,self.ticked)

    def CountCellNeighbours(self, w, h):
        count = 0
        lowXRange = -1
        highXRange = 2
        lowYRange = -1
        highYRange = 2

        if w == 0:
            lowXRange = 0
        elif w == self.width-1:
            highXRange = 1
        if h == 0:
            lowYRange = 0
        elif h == self.heigth-1:
            highYRange = 1


        for x in range(lowXRange,highXRange):
            for y in range(lowYRange,highYRange):
                #print(w, h, lowXRange, highXRange, lowYRange, highYRange, x, y)
                if self.board[w+x][h+y] >= 1:
                    count = count + 1
        if count > 1:
            count = count - 1
        return count

    def ticked(self):
        survivor = 0
        birth = 0
        death = 0

        for w in range(0,self.width):
            self.nextGen.append([])
            for h in range(self.heigth):
                neighbours = self.CountCellNeighbours(w,h)
                if self.board[w][h] >= 1:
                    # This is a living cell
                    if neighbours == 2 or neighbours == 3:
                        # Survive
                        self.nextGen[w].append(self.board[w][h] + 1)
                        survivor += 1
                    else:
                        # Death
                        self.nextGen[w].append(0)
                        death += 1
                else:
                    # This cell is dead
                    if neighbours == 2:
                        # Birth
                        self.nextGen[w].append(self.board[w][h] + 1)
                        birth += 1
                    else:
                        # Death
                        self.nextGen[w].append(0)
                        death += 1

        self.board = self.nextGen
        self.nextGen = []
        self.generation += 1

        print('gen ', self.generation, ': survivor ', survivor, ', birth ', birth, ', death ', death)

        Wdrawing.repaint()


# Main start
app = QtWidgets.QApplication(sys.argv) 

window = QWidget()
layout = QVBoxLayout()
window.setLayout(layout)

row = 10
line = 10

global game
game = GameController(row, line)

global Wdrawing
Wdrawing = Drawing()
Wdrawing.setFixedSize(row * cell_size,line * cell_size)

# Create layout for GUI
LGui = QHBoxLayout()

layout.addLayout(LGui)
layout.addWidget(Wdrawing)
# show and start
window.show()
sys.exit(app.exec_())