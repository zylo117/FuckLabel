import sys

import cv2
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QThread, QEvent
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog
from ui import Ui_MainWindow

import cgitb

cgitb.enable()  # Enable hidden errors and warnings, especially important for windows PYQT

import numpy as np


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.pic.setScaledContents(True)

        self.active_labels = []

        self.image_paths = []

        self.loadImg.clicked.connect(self.load_img)

        # init pic
        self.pic_real_w = 1
        self.pic_real_h = 1
        self.current_image_index = 0
        self.load_pic('home.jpg')
        self.set_pic()

        # init button
        self.next.clicked.connect(lambda: self.load_next(previous=False))
        self.previous.clicked.connect(lambda: self.load_next(previous=True))

        # start a mouse pos monitoring thread
        app.installEventFilter(self)
        self.mouse = MousePos()
        self.mouse_window_x = 0
        self.mouse_window_y = 0
        self.mouse.start()

    def load_next(self, previous=False):
        if previous:
            self.current_image_index -= 1 if self.current_image_index > 0 else 0
        else:
            self.current_image_index += 1 if self.current_image_index < len(self.image_paths) else len(
                self.image_paths) - 1
        try:
            if self.current_image_index >= 0:
                self.load_pic(self.image_paths[self.current_image_index])
                self.set_pic()
        except IndexError:
            # restore current_image_index
            if previous:
                self.current_image_index += 1
            else:
                self.current_image_index -= 1
            pass

    def load_pic(self, img_path):
        self.current_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    def set_pic(self, img=None):
        if img is None:
            img = self.current_img

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = img.shape
        self.pic_real_h, self.pic_real_w = height, width
        pile_width = channel * width

        q_image = QImage(img.data, width, height, pile_width, QImage.Format_RGB888)

        # adapt window
        monitor_width, monitor_height = self.pic.width(), self.pic.height()
        monitor_ratio = monitor_width / monitor_height
        video_ratio = width / height
        if monitor_ratio - video_ratio > 0.1:
            # considering calculation precision error issue, don't use "!=" to judge
            qpix = QPixmap.fromImage(q_image).scaled(width * monitor_height / height, monitor_height)
        elif monitor_ratio - video_ratio < 0.1:
            qpix = QPixmap.fromImage(q_image).scaled(monitor_width, height * monitor_width / width)
        self.pic.setPixmap(qpix)

    # def paintEvent(self, event):
    #     self.painter = QPainter()
    #     self.painter.begin(self)
    #     pen = QPen(Qt.red, 2, Qt.SolidLine)
    #     self.painter.setPen(pen)

    def mousePressEvent(self, e):  ##重载一下鼠标点击事件
        # 左键按下
        if e.buttons() == QtCore.Qt.LeftButton:
            print('fuck')

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

    def load_img(self):
        self.image_paths = self.file_select_dialog('选择图片')
        self.image_paths = self.image_paths[0]

        # load the first image
        self.load_pic(self.image_paths[0])
        self.set_pic()

    def file_select_dialog(self, dialog_name, path_select=False, default_path=None, *filter):
        # filter_str = filter
        # file_path, current_filter = QFileDialog.getOpenFileNames(self, dialog_name, default_path, "Text Files (*.txt);;All Files (*)")
        if not path_select:
            file_path, current_filter = QFileDialog.getOpenFileNames(self, dialog_name, default_path,
                                                                     "Image Files (*.jpg);;All Files (*)")
            return file_path, current_filter
        else:
            path = QFileDialog.getExistingDirectory(self, dialog_name, default_path)
            return path


class MousePos(QThread):
    def __init__(self):
        super(MousePos, self).__init__()
        self.old_x = -1
        self.old_y = -1

    def run(self):
        while True:
            self.show_co()
            self.msleep(10)

    def show_co(self):
        mouse_x = mainWindow.mouse_window_x
        mouse_y = mainWindow.mouse_window_y

        pic_x = mainWindow.pic.x()
        pic_y = mainWindow.pic.y()
        pic_w = mainWindow.pic.width()
        pic_h = mainWindow.pic.height()

        if (mouse_x != self.old_x or mouse_y != self.old_y) and (
                pic_x < mouse_x < pic_w + pic_x and pic_y < mouse_y < pic_h + pic_y):
            self.old_x = mouse_x
            self.old_y = mouse_y

            monitor_x = mouse_x - pic_x
            monitor_y = mouse_y - pic_y

            monitor_x *= mainWindow.pic_real_w / pic_w
            monitor_y *= mainWindow.pic_real_h / pic_h

            print(monitor_x, monitor_y)


# setup GUI
app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()

sys.exit(app.exec_())
