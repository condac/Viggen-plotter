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

from pathlib import Path
import XPlaneUdp
import bild
import bild2
import bild3
import bild4
import bild5
import bild6

#LISTEN_PORT = 49006
SEND_PORT = 49000
XPLANE_IP = "127.0.0.1"


# Egna  funktioner
current_milli_time = lambda: int(round(time.time() * 1000))


parser = argparse.ArgumentParser()

parser.add_argument("--ip", help="Ip address of X-plane")
args = parser.parse_args()

if args.ip:
    XPLANE_IP = args.ip
print ("Connecting to ", XPLANE_IP)

def signal_handler(sig, frame):
        print("You pressed Ctrl+C!")
        running = False
        sys.exit(0)
        os._exit(0)


class RunGUI(QMainWindow):
    def __init__(self,):
        super(RunGUI,self).__init__()

        
        self.buttonList = []
        self.xp = XPlaneUdp.XPlaneUdp(XPLANE_IP,SEND_PORT)
        self.getVariables()
        
        bild1 = bild.Bild(self)
        bild1.show()
        bild22 = bild2.Bild2(self)
        bild22.show()
        bild33 = bild3.Bild(self)
        bild33.show()
        bild44 = bild4.Bild(self)
        bild44.show()
        bild55 = bild5.Bild(self)
        bild55.show()
        bild66 = bild6.Bild(self)
        bild66.show()
        
        self.initUI()
        
    def getVariables(self):
        self.mass = self.xp.getDataref("sim/flightmodel/weight/m_total",10)
        self.alfa = self.xp.getDataref("sim/flightmodel/position/alpha",10)
        self.mach = self.xp.getDataref("sim/flightmodel/misc/machno",10)
        self.kmh = self.xp.getDataref("sim/flightmodel/position/indicated_airspeed",10) * 1.852
        self.hojd = self.xp.getDataref("sim/flightmodel/misc/h_ind",10) * 0.3048
        self.drag = self.xp.getDataref("sim/flightmodel/forces/drag_path_axis",10)
        self.motorTotalt  = self.xp.getDataref("sim/cockpit2/engine/indicators/thrust_n[0]",10)
        self.motorDry = self.xp.getDataref("sim/cockpit2/engine/indicators/thrust_dry_n[0]",10)
        self.motorEBK = self.motorTotalt - self.motorDry
        self.fuelflowDry = self.xp.getDataref("sim/cockpit2/engine/indicators/fuel_flow_dry_kg_sec[0]",10)
        self.fuelflow = self.xp.getDataref("sim/cockpit2/engine/indicators/fuel_flow_kg_sec[0]",10)
        self.fuelProcentMin = self.fuelflow * 60 /42
        self.fuelProcentMinDry = self.fuelflow * 60 /42
        #print(self.mach, self.kmh, self.hojd,self.drag,self.motorTotalt,self.motorDry,self.motorEBK)
        
    def initUI(self):
        #self.root = Tk() # for 2d drawing
        
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(current_dir, "../ui/main.ui"), self)
        print(self.ui)
        #self.setGeometry(200, 200, 300, 300)
        #self.resize(640, 480)
        self.setWindowTitle("Logger")
        
        
        # connectButton(self, self.ui.button_afk,"JAS/button/afk")
        # connectButton(self, self.ui.button_hojd,"JAS/button/hojd")
        # connectButton(self, self.ui.button_att,"JAS/button/att")
        
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.loop)
        self.timer.start(100)



    def updateGUI(self):
        
        pass
        
        

                
    def loop(self):
        self.xp.readData()
        self.getVariables()
        self.updateGUI()
        
        #print(self.xp.dataList)
        self.timer.start(10)
        pass
        

if __name__ == "__main__":

    try:
        app = QApplication(sys.argv)
        win = RunGUI()
        win.show()
        sys.exit(app.exec_())
    except Exception as err:
        exception_type = type(err).__name__
        print(exception_type)
        print(traceback.format_exc())
        os._exit(1)
    print ("program end")
    os._exit(0)
