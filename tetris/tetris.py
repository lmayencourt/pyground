import sys, math, random
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randint
from pieces import Piece

class Drawing(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFocusPolicy( Qt.StrongFocus )

        self.brush = QBrush(QColor(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))        # set fillColor  
        self.pen = QPen(QColor(0,0,0,0))                      # set lineColor
        self.pen.setWidth(1)                                            # set lineWidth

        self.colors = []

        self.trans = [5,5,0]
        self.rot = [0,0,0]
        self.viewPoint = 200
        self.cubeSize = 25

        self.pieces = []
        for i in range(7):
            self.pieces.append(Piece(i,self.cubeSize))
            self.pieces[i].setPos([i*self.cubeSize,self.cubeSize*i*4,0])
            #self.piece[i].setColor(QColor(20,50,self.cubeSize*i,100))

    def setTranslation(self,trans):
        for i in range(3):
            self.trans[i] = trans[i]*2-100
        self.repaint()

    def setRotation(self,rot):
        for i in range(3):
            self.rot[i] = rot[i]/100
        self.repaint()

    def createColors(self,base,nbr):
        self.colors.clear()

        for i in range(0,nbr):
            rgb = []
            rgb.append(self.baseColor.red())
            rgb.append(self.baseColor.green())
            rgb.append(self.baseColor.blue())
            for i in range(3):
                if rgb[i] < 125:
                    rgb[i] += random.randint(0,124)
                else:
                    rgb[i] -= random.randint(0,125)
            self.colors.append(QColor(rgb[0], rgb[1], rgb[2], 100))

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        for w in range(1,game.width+1):
            for h in range(game.heigth+1):
                self.brush = QColor(0,0,game.gametab[w][h]*100,100)
                self.pen = QPen(QColor(255,255,255,255))
                painter.setBrush(self.brush)
                painter.drawRect(w*20,h*20,20,20)

        for x in range(4):
            for y in range(4):
                if game.pieceType[x][y]:
                    self.brush = QColor(0,game.pieceType[x][y]*100,0,100)
                    painter.setBrush(self.brush)
                    painter.drawRect((game.piecePos[0]+x)*20,(game.piecePos[1]+y)*20,20,20)
                if game.pieceNext[x][y]:
                    self.brush = QColor(0,100,0,100)
                    painter.setBrush(self.brush)
                    painter.drawRect((x+game.width+2)*20,(y+game.heigth//2-4)*20,20,20)
                    #print(x,y,game.pieceType[x][y])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            game.rotation()
        if event.key() == Qt.Key_Down:
            game.move(1)
        if event.key() == Qt.Key_Left:
            game.move(2)
        if event.key() == Qt.Key_Right:
            game.move(3)

        self.repaint() 

class Letter():
    def __init__(self, char):
        self.char = char    

class GameController():
    def __init__(self,width,heigth):
        self.width = width
        self.heigth = heigth

        self.piecePos = [width//2,-2]
        self.pieceType = self.getPieceTab(randint(0,6))
        self.pieceNext = self.getPieceTab(randint(0,6))

        self.gametab = []
        for w in range(width+2):
            self.gametab.append([])
            for h in range(heigth+1):
                if h == heigth or w == 0 or w == width:
                    self.gametab[w].append(1)
                else:
                    self.gametab[w].append(0)

        self.tick = QTimer()
        self.tick.timeout.connect(self.ticked)
        self.tick.start(1000)

    def ticked(self):
        print('tick',self.pieceType,self.piecePos)


        if self.detectDownCollision():
            # collided
            for x in range(4):
                for y in range(4):
                    self.gametab[self.piecePos[0]+x][self.piecePos[1]+y] |= self.pieceType[x][y]

            self.piecePos = [self.width//2,-2]
            self.pieceType = self.pieceNext
            self.pieceNext = self.getPieceTab(randint(0,6))

            # detect full line
            for y in range(self.heigth):
                acc = 0
                for x in range(self.width):
                    acc += self.gametab[x][y]
                if acc == self.width:
                    # full line, move everything down
                    for a in range(y):
                        for b in range(1,self.width-1):
                            self.gametab[b][y- a] = self.gametab[b][y - a - 1]
        else:
            # move pice down
            self.piecePos[1] = self.piecePos[1] + 1

        Wdrawing.repaint()

    def detectDownCollision(self):
        collided = 0
        for i in range(4):
            if self.gametab[self.piecePos[0]+i][self.piecePos[1]+4] == 1 and self.pieceType[i][3]:
                collided = 1
            if self.gametab[self.piecePos[0]+i][self.piecePos[1]+3] == 1 and self.pieceType[i][2]:
                collided = 1

        return collided

    def detectLeftCollision(self):
        collided = 0
        for i in range(2,4):
            if self.gametab[self.piecePos[0]-1][self.piecePos[1]+i] == 1 and self.pieceType[0][i]:
                collided = 1

        return collided

    def detectRightCollision(self):
        collided = 0
        for i in range(1,4):
            for y in range(2,4):
                if self.gametab[self.piecePos[0]+i+1][self.piecePos[1]+y] == 1 and self.pieceType[i][y]:
                    collided = 1

        return collided

    def move(self,dir):
        # up, down, left, right
        if dir == 0:
                self.piecePos[1] += 1
        if dir == 1:
            if self.detectDownCollision() == 0:
                self.piecePos[1] += 1
        if dir == 2:
            if self.detectLeftCollision() == 0:
                self.piecePos[0] -= 1
        if dir == 3:
            if self.detectRightCollision() == 0:
                self.piecePos[0] += 1

    def rotation(self):
        newPiece = self.getPieceTab(0)
        for x in range(4):
            for y in range(4):
                newPiece[x][y] = self.pieceType[3-y][x]

        if newPiece[0][2] == 0 or newPiece[0][3] == 0:
            for x in range(3):
                for y in range(4):
                    newPiece[x][y] = newPiece[x+1][y]
            for y in range(4):
                newPiece[3][y] = 0

        if not newPiece[0][3] and not newPiece[1][3] and not newPiece[2][3] and not newPiece[3][3]:
            for x in range(4):
                for y in range(3):
                    newPiece[x][3-y] = newPiece[x][2-y]

        self.pieceType = newPiece

    def getPieceTab(self,type):
        pieceList = {
            0:[[0,0,0,1],[0,0,0,1],[0,0,0,1],[0,0,0,1]], #l
            1:[[0,0,1,1],[0,0,1,1],[0,0,0,0],[0,0,0,0]], #o
            2:[[0,0,1,0],[0,0,1,1],[0,0,1,0],[0,0,0,0]], #t
            3:[[0,0,1,1],[0,0,0,1],[0,0,0,1],[0,0,0,0]], #L
            4:[[0,0,0,1],[0,0,0,1],[0,0,1,1],[0,0,0,0]], #J
            5:[[0,0,1,0],[0,0,1,1],[0,0,0,1],[0,0,0,0]], #z
            6:[[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,0,0,0]], #s
        }

        return pieceList.get(type)

class Control3D(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.layout = QVBoxLayout()
        self.Sxyz = []
        self.Lxyz = []
        latext = ['x','y','z']
        for i in range(3):
            xlayout = QHBoxLayout()
            self.Lxyz.append(QLabel(latext[i]))
            self.Sxyz.append(QSlider(Qt.Horizontal))
            self.Sxyz[i].setMinimum(0)
            self.Sxyz[i].setMaximum(100)
            self.Sxyz[i].valueChanged.connect(self.sliderChange)
            xlayout.addWidget(self.Lxyz[i])
            xlayout.addWidget(self.Sxyz[i])
            self.layout.addLayout(xlayout)

        self.setLayout(self.layout)

    def setCallback(self,callback):
        self.callback = callback

    def sliderChange(self):
        xyz = []
        for i in range(3):
            xyz.append(self.Sxyz[i].value())

        self.callback(xyz)

# Main start
app = QtWidgets.QApplication(sys.argv) 

window = QWidget()
layout = QVBoxLayout()
window.setLayout(layout)

global game
game = GameController(12,12)

global Wdrawing
Wdrawing = Drawing()
Wdrawing.setFixedSize(400,500)

# Create layout for GUI
LGui = QHBoxLayout()

C3Dtrans = Control3D()
C3Dtrans.setCallback(Wdrawing.setTranslation)
LGui.addWidget(C3Dtrans)

C3Drot = Control3D()
C3Drot.setCallback(Wdrawing.setRotation)
LGui.addWidget(C3Drot)

layout.addLayout(LGui)
layout.addWidget(Wdrawing)
# show and start
window.show()
sys.exit(app.exec_())