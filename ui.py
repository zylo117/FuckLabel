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
        MainWindow.resize(1024, 696)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pic = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pic.sizePolicy().hasHeightForWidth())
        self.pic.setSizePolicy(sizePolicy)
        self.pic.setMinimumSize(QtCore.QSize(600, 600))
        self.pic.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.pic.setMouseTracking(True)
        self.pic.setAutoFillBackground(True)
        self.pic.setScaledContents(True)
        self.pic.setObjectName("pic")
        self.horizontalLayout.addWidget(self.pic)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout.addWidget(self.line_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.thinner = QtWidgets.QPushButton(self.centralwidget)
        self.thinner.setObjectName("thinner")
        self.gridLayout_3.addWidget(self.thinner, 1, 0, 1, 1)
        self.shorter = QtWidgets.QPushButton(self.centralwidget)
        self.shorter.setObjectName("shorter")
        self.gridLayout_3.addWidget(self.shorter, 2, 1, 1, 1)
        self.wider = QtWidgets.QPushButton(self.centralwidget)
        self.wider.setObjectName("wider")
        self.gridLayout_3.addWidget(self.wider, 1, 2, 1, 1)
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setObjectName("reset")
        self.gridLayout_3.addWidget(self.reset, 1, 1, 1, 1)
        self.taller = QtWidgets.QPushButton(self.centralwidget)
        self.taller.setObjectName("taller")
        self.gridLayout_3.addWidget(self.taller, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.previous = QtWidgets.QPushButton(self.centralwidget)
        self.previous.setObjectName("previous")
        self.verticalLayout.addWidget(self.previous)
        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setObjectName("next")
        self.verticalLayout.addWidget(self.next)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.piclist = QtWidgets.QListView(self.centralwidget)
        self.piclist.setObjectName("piclist")
        self.verticalLayout.addWidget(self.piclist)
        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(6, 3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.setStretch(0, 8)
        self.horizontalLayout.setStretch(2, 2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)
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
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(2, 9)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_Images = QtWidgets.QAction(MainWindow)
        self.actionLoad_Images.setObjectName("actionLoad_Images")
        self.actionLoad_JSON = QtWidgets.QAction(MainWindow)
        self.actionLoad_JSON.setObjectName("actionLoad_JSON")
        self.actionSave_JSON = QtWidgets.QAction(MainWindow)
        self.actionSave_JSON.setObjectName("actionSave_JSON")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FuckLabel"))
        self.pic.setText(_translate("MainWindow", "TextLabel"))
        self.thinner.setText(_translate("MainWindow", "变窄"))
        self.shorter.setText(_translate("MainWindow", "变矮"))
        self.wider.setText(_translate("MainWindow", "变宽"))
        self.reset.setText(_translate("MainWindow", "重置"))
        self.taller.setText(_translate("MainWindow", "变高"))
        self.previous.setText(_translate("MainWindow", "上一张"))
        self.next.setText(_translate("MainWindow", "下一张"))
        self.label_2.setText(_translate("MainWindow", "图片列表"))
        self.loadJSON.setText(_translate("MainWindow", "保存JSON"))
        self.loadImg.setText(_translate("MainWindow", "载入图片"))
        self.saveJSON.setText(_translate("MainWindow", "载入JSON"))
        self.actionLoad_Images.setText(_translate("MainWindow", "Load Images"))
        self.actionLoad_JSON.setText(_translate("MainWindow", "Load JSON"))
        self.actionSave_JSON.setText(_translate("MainWindow", "Save JSON"))

