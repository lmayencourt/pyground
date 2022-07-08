import sys, math, random
import numpy as np
from PyQt5.QtGui import QColor, QPolygon
from PyQt5.QtCore import QPoint

class Piece():
    def __init__(self,type,size):
        pieceList = {
            0:self.l,
            1:self.o,
            2:self.t,
            3:self.L,
            4:self.J,
            5:self.z,
            6:self.s
        }

        self.size = size
        constructor = pieceList.get(type,self.L())
        self.cubeList = constructor()

    def l(self):
        piece = []
        for i in range(4):
            piece.append(Cube())
            piece[i].setSize(self.size)
            if i <2:
                piece[i].setPos([i*self.size,0,0])
            else:
                piece[i].setPos([(i%2)*self.size,self.size,0])
        return piece

    def o(self):
        piece = []
        for i in range(4):
            piece.append(Cube())
            piece[i].setSize(self.size)
            if i <2:
                piece[i].setPos([i*self.size,0,0])
            else:
                piece[i].setPos([(i%2)*self.size,self.size,0])
        return piece

    def t(self):
        piece = []
        for i in range(4):
            piece.append(Cube())
            piece[i].setSize(self.size)
            if i<3:
                piece[i].setPos([i*self.size,self.size,0])
            else:
                piece[i].setPos([self.size,0,0])
        return piece

    def L(self):
        piece = []
        for i in range(4):
            piece.append(Cube())
            piece[i].setSize(self.size)
            if i<3:
                piece[i].setPos([0,i*self.size,0])
            else:
                piece[i].setPos([self.size,2*self.size,0])
        return piece

    def J(self):
        piece = []
        for i in range(4):
            piece.append(Cube())
            piece[i].setSize(self.size)
            if i<3:
                piece[i].setPos([self.size,i*self.size,0])
            else:
                piece[i].setPos([0,2*self.size,0])
        return piece

    def z(self):
        piece = []
        for i in range(4):
            piece.append(Cube())
            piece[i].setSize(self.size)
            if i <2:
                piece[i].setPos([i*self.size,0,0])
            else:
                piece[i].setPos([(1+i%2)*self.size,self.size,0])
        return piece

    def s(self):
        piece = []
        for i in range(4):
            piece.append(Cube())
            piece[i].setSize(self.size)
            if i <2:
                piece[i].setPos([i*self.size,self.size,0])
            else:
                piece[i].setPos([(1+i%2)*self.size,0,0])
        return piece

    def setPos(self,pos):
        for cube in self.cubeList:
            cube.setPos(pos)

class Cube():
    def __init__(self):
        self.cubeSize = 50
        self.color = QColor(20,50,200,140)

        self.createCube(self.cubeSize)

    def setColor(self,color):
        self.color = color

    def setSize(self,size):
        self.cubeSize = size
        self.createCube(size)

    def setPos(self,pos):
        self.matrix = self.translation(self.matrix,pos[0],pos[1],pos[2])

    def createCube(self,size):
        self.matrix = np.array([[0,0,0,1],\
                            [size,0,0,1],\
                            [size,size,0,1],\
                            [0,size,0,1],\
                            [0,0,-size,1],\
                            [size,0,-size,1],\
                            [size,size,-size,1],\
                            [0,size,-size,1]])

        self.matrix = self.translation(self.matrix,-size/2,-size/2,size/2)

    def getCubeView(self,viewPoint,trans,rot):
        proj = np.array([[1,0,0,0],\
                          [0,1,0,0],\
                          [0,0,0,-1/viewPoint],\
                          [0,0,0,1]])

        v = self.rotation(self.matrix,rot[0],rot[1],rot[2])
        v = self.translation(v,trans[0],trans[1],trans[2])
        v = v.dot(proj)

        self.faces = []

        points = [[0,1,2,3],[4,5,6,7],[2,3,7,6],[0,1,5,4],[0,3,7,4],[1,2,6,5]]
        for y in range(6):
            self.faces.append(QPolygon())
            offset = 5*self.cubeSize
            for i in points[y]:
               # print(points[y], "->", i,"= ", v[i][0]/v[i][3], ",",v[i][1]/v[i][3])
                self.faces[y] << QPoint(v[i][0]/v[i][3]+offset, v[i][1]/v[i][3]+offset)

        return self.faces

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