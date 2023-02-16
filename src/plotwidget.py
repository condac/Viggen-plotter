from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy
from PyQt5.QtCore import QTimer, Qt,QRect
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor, QPalette, QPixmap
from PyQt5.QtGui import *
import json
#from pathlib import Path

#import argparse
import datetime
import os
import time
import traceback
import sys
import colorsys
import random
#import math
import threading

#Egna saker
import sys



def getS(r, n, xs):
    x = xs/100.0
    for i in range(n):
        x = r*x*(1-x)
    return x

def mapValue(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class ImageCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        scroll_area = QtWidgets.QScrollArea(widgetResizable=True)
        self.dw = DrawWidget()
        scroll_area.setWidget(self.dw)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(scroll_area)
        self.setWindowTitle("2D Qt")
        #self.resize(850, 650)


class BitPlot(QWidget):
    def __init__(self, parent, x=1000, y=400, image="../bilder/bild1.png"):
        print("new plot", x, y)
        super().__init__()
        self.parent = parent
        self.setWindowTitle("2D Qt")
        #self.resize(800, 1100)
        self.infoX = 300
        self.imageurl = image
        
        ir = QImageReader(str(self.imageurl))
        size = ir.size()
        if size.isValid():
            
            self.paperX = size.width()
            self.paperY = size.height()
        else:
            self.paperX = 800
            self.paperY = 600
        self.imageX = self.paperX+20
        self.imageY = self.paperY
        

        #self.setMinimumSize(int(self.imageX), int(self.imageY))
        self.resize(int(self.imageX), int(self.imageY))
        self.buffer = QPixmap(int(self.paperX), int(self.paperY))

        self.painter = QPainter(self)
        # set black background
        #r, g, b = self.hsv2rgb(1.0, 1.0, 1.0)
        self.backgroundColor = QColor(255, 255, 255)

        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(10, 10, 10))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        #self.setFixedSize(3000, self.Ysize)
        self.parent.resize(int(self.imageX), int(self.imageY+60))
        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.x = 0.0
        self.y = 0.4
        self.r = 2.0
        self.prevY = 0.0
        self.timestart = 0.0
        self.prevIntTime = int(0)
        self.prevTime = 0.0
        self.colorRotation = 0.0
        self.colorStep = 0.29*2
        self.showInfo = False

        self.paperTime = 15*60
        self.timeStep = self.paperTime/self.paperX

        

        self.d_clock = 0.0
        self.d_clock_prev = 0.0
        self.points = []
        self.varList = []
        self.varList.append("status")

        self.newPaper()

        # self.lock = threading.Lock()
        # self.netthread = NetThread(self)
        # self.netthread.start()

    def getPaperX(self):
        return self.paperX

    def getPaperY(self):
        return self.paperY

    def setXScaleStart(self, x, y, minvalue):
        self.xscale_start_x = x
        self.xscale_start_y = y
        
        self.xscale_min = minvalue
        
    def setXScaleEnd(self, x, y, maxvalue):
        self.xscale_end_x = x
        self.xscale_end_y = y
        
        self.xscale_max = maxvalue
                
    def setYScaleStart(self, x, y, minvalue):
        self.yscale_start_x = x
        self.yscale_start_y = y
        
        self.yscale_min = minvalue
        
    def setYScaleEnd(self, x, y, maxvalue):
        self.yscale_end_x = x
        self.yscale_end_y = y
        
        self.yscale_max = maxvalue
                
        
    def drawPointR(self, x=0, y=0):
        hue = self.colorRotation
        self.colorRotation += self.colorStep
        while(self.colorRotation>1.0):
            self.colorRotation -= 1.0
        r,g,b = self.hsv2rgb(hue, 1.0, 1.0)
        color1 = QColor( r,g,b )
        self.drawPoint(x, y, color1)
         
    def drawPoint(self, x, y, color1):
        self.painter.begin(self.buffer)
        
        
        
        self.painter.setPen(QPen(color1, 4, Qt.SolidLine))
        x = self.xscale_start_x + mapValue(x, self.xscale_min, self.xscale_max, 0, self.xscale_end_x-self.xscale_start_x)
        y = self.yscale_start_y - mapValue(y, self.yscale_min, self.yscale_max, 0, self.yscale_start_y-self.yscale_end_y)
        x = int(x)
        y = int(y)
        print("ritar x", x, "y", y, "papper", self.paperY, self.yscale_start_y)
        self.painter.drawLine(x, y, x+1, y+1)
        
        #self.painter.drawLine(0, self.yscale_start_y, 0+1, self.paperY+1)
        self.painter.end()
        
    def newPaper(self):
        self.imageX = self.paperX+20
        self.imageY = self.paperY+20

        #self.setMinimumSize(int(self.imageX), int(self.imageY))
        self.resize(int(self.imageX), int(self.imageY))
        # self.lock.acquire()
        #oldpaper = self.buffer
        self.buffer = QPixmap(int(self.paperX), int(self.paperY))
        self.painter.begin(self.buffer)

        #self.painter.drawPixmap(xpos, 0, xresize, self.paperY, oldpaper)
        self.painter.drawImage(QRect(0, 0, self.paperX, self.paperY), QImage(self.imageurl))

        self.painter.end()
        # self.lock.release()

    def setPaperTime(self, s):
        self.paperTime = s


    def paintEvent(self, e):
        #self.painter = QPainter(self)
        # lockRes = self.lock.acquire(timeout=0.5)
        # if lockRes:
            self.painter.begin(self)
            
            infoX = 0
            showInfo = False

            if (self.showInfo):
                infoX = self.infoX
            else:
                infoX = 0

            
            
            self.painter.drawPixmap(0-infoX, 0, self.buffer) #load graph from Bitmap


            row = 0
            self.painter.setFont(QFont('Decorative', 10))
            for point in self.points:
                self.painter.setPen(QPen(point["color"], point["penSize"]+2, Qt.SolidLine))
                try:
                    val = float(point["value"])
                except:
                    val = 0.0
                value = mapValue(val, point["min"], point["max"], 0, self.paperY-2)

                x = int(self.paperX+1)-infoX
                y = self.paperY - int(value) -1
                if (y>self.paperY):
                    y = self.paperY
                if (y<0):
                    y = 0
                if y<self.paperY+2 and y>-1000:
                    self.painter.drawLine(x, y, x+20, y)
                if (self.showInfo):
                    #self.painter.setFont(QFont('Decorative', 10))
                    self.painter.drawText(self.paperX+25-infoX, 20+row*20, f"{point['simvar']} = {point['value']}")
                row+=1
            self.painter.end()
            # self.lock.release()

    def hsv2rgb(self,h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    def addNew(self, simvar, min=0, max=100, col=0, row=0, color=None):
        if (color):
            color1 = QColor( color )
            #color1 = QColor( "#ff00ff" )
        else:
            #color = QColor(int(random.random()*255), int(random.random()*255), int(random.random()*255))
            hue = self.colorRotation
            self.colorRotation += self.colorStep
            while(self.colorRotation>1.0):
                self.colorRotation -= 1.0
            r,g,b = self.hsv2rgb(hue, 1.0, 1.0)
            color1 = QColor( r,g,b )

        point = {}
        point["simvar"] = simvar
        point["min"] = min
        point["max"] = max
        point["color"] = color1
        point["prevY"] = 0.0
        point["value"] = 0.0
        point["penSize"] = 1
        self.points.append(point)
        self.varList.append(point["simvar"])
        #print(self.varList)


    def redraw(self):
        #self.updateValues()
        self.update()
        #self.timer.start(50)




if __name__ == "__main__":
    
    try:
        app = QApplication(sys.argv)
        win = ImageCanvas()
        win.show()
        sys.exit(app.exec_())

    except Exception as err:
        exception_type = type(err).__name__
        print(exception_type)
        print(traceback.format_exc())
        os._exit(1)
    print ("program end")
    os._exit(0)