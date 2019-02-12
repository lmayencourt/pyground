import sys, math, random
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randint
from pieces import Piece

class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
   
        self.brush = QBrush(QColor(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))        # set fillColor  
        self.pen = QPen(QColor(0,0,0,0))                      # set lineColor
        self.pen.setWidth(1)                                            # set lineWidth

        self.baseColor = QtGui.QColor(20,50,200,255)
        self.colors = []
        self.createColors(self.baseColor,6)

        self.trans = [5,5,0]
        self.rot = [0,0,0]
        self.viewPoint = 200
        self.cubeSize = 100

        self.createCube(self.cubeSize)
        self.createCubeView(self.A,self.viewPoint,self.trans,self.rot)

    def createCube(self,size):
        self.A = np.array([[0,0,0,1],\
                            [size,0,0,1],\
                            [size,size,0,1],\
                            [0,size,0,1],\
                            [0,0,-size,1],\
                            [size,0,-size,1],\
                            [size,size,-size,1],\
                            [0,size,-size,1]])

        self.A = self.translation(self.A,-size/2,-size/2,size/2)

    def createCubeView(self,cube,viewPoint,trans,rot):
        proj = np.array([[1,0,0,0],\
                          [0,1,0,0],\
                          [0,0,0,-1/viewPoint],\
                          [0,0,0,1]])

        v = self.rotation(cube,rot[0],rot[1],rot[2])
        v = self.translation(v,trans[0],trans[1],trans[2])
        v = v.dot(proj)

        self.faces = []

        points = [[0,1,2,3],[4,5,6,7],[2,3,7,6],[0,1,5,4],[0,3,7,4],[1,2,6,5]]
        for y in range(6):
            self.faces.append(QtGui.QPolygon())
            offset = 2*self.cubeSize
            for i in points[y]:
               # print(points[y], "->", i,"= ", v[i][0]/v[i][3], ",",v[i][1]/v[i][3])
                self.faces[y] << QPoint(v[i][0]/v[i][3]+offset, v[i][1]/v[i][3]+offset)

    def translation(self,obj,x,y,z):
        Mtrans = np.array([[1,0,0,0],
                          [0,1,0,0],\
                          [0,0,1,0],\
                          [x,y,z,1]])

        return obj.dot(Mtrans)

    def rotation(self,obj,x,y,z):
        Mrotx = np.array([[1,0,0,0],\
                          [0,math.cos(x),math.sin(x),0],\
                          [0,-math.sin(x),math.cos(x),0],\
                          [0,0,0,1]])
        Mroty = np.array([[math.cos(y),0,-math.sin(y),0],\
                          [0,1,0,0],\
                          [math.sin(y),0,math.cos(y),0],\
                          [0,0,0,1]])
        Mrotz = np.array([[math.cos(z),math.sin(z),0,0],\
                          [-math.sin(z),math.cos(z),0,0],\
                          [0,0,1,0],\
                          [0,0,0,1]])

        return obj.dot(Mrotx.dot(Mroty.dot(Mrotz)))

    def setTranslation(self,trans):
        self.trans = trans
        self.createCubeView(self.A,self.viewPoint,self.trans,self.rot)
        self.repaint()

    def setRotation(self,rot):
        for i in range(3):
            #self.rot[i] = rot[i]*math.pi/50 - math.pi
            self.rot[i] = rot[i]/100
        self.createCubeView(self.A,self.viewPoint,self.trans,self.rot)
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
        for i,face in enumerate(self.faces):
                # set brush (fill) and pen (line) color
                self.brush = QBrush(self.colors[i])
                self.pen = QPen(QColor(0,0,0,0))                      # set lineColor
                #self.pen = QPen(color)                      # set lineColor
                self.pen.setWidth(1)                                            # set lineWidth
                painter.setBrush(self.brush)
                painter.drawPolygon(face)

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

global Wdrawing
Wdrawing = MyWidget()

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