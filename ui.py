# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.loadJSON = QtWidgets.QPushButton(self.centralwidget)
        self.loadJSON.setObjectName("loadJSON")
        self.gridLayout.addWidget(self.loadJSON, 0, 2, 1, 1)
        self.loadImg = QtWidgets.QPushButton(self.centralwidget)
        self.loadImg.setObjectName("loadImg")
        self.gridLayout.addWidget(self.loadImg, 0, 0, 1, 1)
        self.saveJSON = QtWidgets.QPushButton(self.centralwidget)
        self.saveJSON.setObjectName("saveJSON")
        self.gridLayout.addWidget(self.saveJSON, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 9)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuLoad = QtWidgets.QMenu(self.menubar)
        self.menuLoad.setObjectName("menuLoad")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_Images = QtWidgets.QAction(MainWindow)
        self.actionLoad_Images.setObjectName("actionLoad_Images")
        self.menuLoad.addAction(self.actionLoad_Images)
        self.menubar.addAction(self.menuLoad.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FuckLabel"))
        self.loadJSON.setText(_translate("MainWindow", "Save JSON"))
        self.loadImg.setText(_translate("MainWindow", "Load Images"))
        self.saveJSON.setText(_translate("MainWindow", "Load JSON"))
        self.menuLoad.setTitle(_translate("MainWindow", "Load"))
        self.actionLoad_Images.setText(_translate("MainWindow", "Load Images"))

