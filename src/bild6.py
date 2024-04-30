#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QTimer,QDateTime, QFile, QTextStream, Qt
from PyQt5.QtGui import QFont

import sys
import json
import random
import argparse
import datetime
import os
import time
import colorsys
import traceback
import threading

from PyQt5.QtGui import *

from pathlib import Path
import XPlaneUdp
import plotwidget

current_milli_time = lambda: int(round(time.time() * 1000))

class Bild(QMainWindow):
    def __init__(self,parent):
        super(Bild,self).__init__()
        self.parent = parent
        self.plot = plotwidget.BitPlot(self, x=1024, y=768,image="../bilder/bild6.png")
        self.plot.setXScaleStart(106, 289, 0.7)
        self.plot.setXScaleEnd(707, 289, 1.5)
        self.plot.setYScaleStart(106, 289, 0)
        self.plot.setYScaleEnd(106, 73, (3*60))
        
        self.tid = 0
        self.startTid = 0
        self.machPrev = 0
        self.initUI()
        
    
    def initUI(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(current_dir, "../ui/bild.ui"), self)
        print(self.ui)
        #self.setGeometry(200, 200, 300, 300)
        self.resize(int(self.plot.getPaperX()), self.plot.getPaperY()+30)
        self.setWindowTitle("Bild6")
        
        self.ui.verticalLayout.addWidget(self.plot)
        
        
        self.ui.pushButton.clicked.connect(self.rensa)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.loop)
        self.timer.start(100)

    def rensa(self):
        self.plot.newPaper()
        
    def loop(self):
        
        if (self.machPrev < 0.775 and self.parent.mach >= 0.775):
            self.startTid = current_milli_time()
            
            
        self.machPrev = self.parent.mach
        self.tid = (current_milli_time() - self.startTid) / 1000
        
        self.plot.drawPoint(self.parent.mach, self.tid,  QColor( 255,0,0 ))
        #self.plot.drawPoint(self.parent.mach, self.parent.fuelProcentMinDry,  QColor( 0,255,0 ))

        #self.plot.drawPoint(self.parent.kmh, self.parent.kmh,  QColor( 0,255,0 ))
        
        #self.plot.drawPoint(self.parent.kmh, self.parent.motorDry,  QColor( 0,255,0 ))
        #self.plot.drawPoint(self.parent.kmh, self.parent.drag,  QColor( 0,0,255 ))
        self.plot.drawPointR(0, 0)
        
        self.plot.redraw()
        pass
