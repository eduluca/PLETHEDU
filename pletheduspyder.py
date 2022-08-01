# -*- coding: utf-8 -*-
"""
Plethysmography GUI code
author: @eduluca
"""
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import pandas as pd
import numpy as np

#%% DATA EXTRACTION (maybe drag and drop into Qtdesign)

#load dataframe from csv
df = pd.read_csv("data.csv")

#print dataframe
print(df)


#%% DATA ORGANIZATION (with pandas library)



#%% GRAPHICAL USER INTERFACE (PyQT5) 

# Might just use QML code on QTDesign Studio instead

 
class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'PLETHEDU'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
    
        self.show()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



#EXTRA FEATURES




#DEBUGGING
