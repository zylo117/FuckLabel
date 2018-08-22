import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QThread, QEvent
from PyQt5.QtGui import QImage, QPixmap, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # start a mouse pos monitoring thread
        app.installEventFilter(self)
        self.mouse = MousePos()
        self.mouse_window_x = 0
        self.mouse_window_y = 0
        self.mouse.start()
        self.active_labels = []

    # override the method to track mouse coordinates
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.NoButton or event.buttons() == Qt.LeftButton:
                pos = event.windowPos()
                self.mouse_window_x = pos.x()
                self.mouse_window_y = pos.y()
            else:
                pass  # do other stuff
        return QMainWindow.eventFilter(self, source, event)

    def resizeEvent(self, event):
        return QMainWindow.resizeEvent(self, event)


class MousePos(QThread):
    def __init__(self):
        super(MousePos, self).__init__()

    def run(self):
        while True:
            self.show_co()
            self.msleep(100)

    def show_co(self):
        mouse_x = mainWindow.mouse_window_x
        mouse_y = mainWindow.mouse_window_y
        print(mouse_x, mouse_y)


# setup GUI
app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()

sys.exit(app.exec_())
