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


class Bild(QMainWindow):
    def __init__(self,parent):
        super(Bild,self).__init__()
        self.parent = parent
        self.plot = plotwidget.BitPlot(self, x=1024, y=768)
        self.plot.setXScaleStart(36, 741, 0.3)
        self.plot.setXScaleEnd(568, 741, 1.1)
        self.plot.setYScaleStart(36, 741, 0.0)
        self.plot.setYScaleEnd(57, 572, 50000)
        
        self.initUI()
        
    
    def initUI(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(current_dir, "../ui/bild.ui"), self)
        print(self.ui)
        #self.setGeometry(200, 200, 300, 300)
        self.resize(int(self.plot.getPaperX()), self.plot.getPaperY()+30)
        self.setWindowTitle("Bild1 Luftmotstånd motorkraft")
        
        self.ui.verticalLayout.addWidget(self.plot)
        self.ui.pushButton.clicked.connect(self.rensa)
        
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.loop)
        self.timer.start(100)

    def rensa(self):
        self.plot.newPaper()
        
    def loop(self):
        self.plot.drawPoint(self.parent.mach, self.parent.motorTotalt,  QColor( 255,0,0 ))
        self.plot.drawPoint(self.parent.mach, self.parent.motorDry,  QColor( 0,255,0 ))
        self.plot.drawPoint(self.parent.mach, self.parent.drag,  QColor( 0,0,255 ))
        self.plot.drawPointR(0.3, 0)
        self.plot.drawPointR(1.1, 100000)
        self.plot.drawPointR(0.3, 50000)
        
        self.plot.redraw()
        pass
