import json
import os
import shutil
import sys

import cv2
import imutils
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QThread, QEvent
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog

from build_json import ImageLabels
from ui import Ui_MainWindow

import cgitb

cgitb.enable()  # Enable hidden errors and warnings, especially important for windows PYQT

import numpy as np

KEY_TEXT = []


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
        self.current_image_filesize = 0
        self.current_image_filename = 'unknown.jpg'
        self.load_pic('home.jpg')
        self.set_pic()
        self.current_label = ''
        self.open_for_label = False

        self.pic_list = []
        self.pic_mask_list = []

        # init button
        self.next.clicked.connect(lambda: self.load_next(previous=False))
        self.previous.clicked.connect(lambda: self.load_next(previous=True))
        self.reset.clicked.connect(self.reset_pic)

        # init painter
        self.draw = 'point'
        self.old_points = []
        self.current_points = []
        self.last_box = []

        # init json
        self.il_buf = ImageLabels('temp_image_labels.json')
        self.loadJSON.clicked.connect(self.load_json)
        self.saveJSON.clicked.connect(self.save_json)

        # start a mouse pos monitoring thread
        app.installEventFilter(self)
        self.pic_real_x = -1
        self.pic_real_y = -1
        self.mouse_window_x = -1
        self.mouse_window_y = -1
        self.mouse = MousePos()
        self.mouse.start()

    def load_next(self, previous=False):
        self.open_for_label = False
        self.current_points = []

        if not previous:
            if self.current_image_index >= len(self.pic_list):
                try:
                    self.pic_list.append(self.current_img)
                    self.pic_mask_list.append(self.current_img_mask)
                except AttributeError:
                    pass

        if previous:
            self.current_image_index -= 1 if self.current_image_index > 0 else 0
        else:
            self.current_image_index += 1 if self.current_image_index < len(self.image_paths) else len(
                self.image_paths) - 1
        try:
            if self.current_image_index >= 0:
                try:
                    self.current_img = self.pic_mask_list[self.current_image_index]
                    self.set_pic()
                except IndexError:
                    self.load_pic(self.image_paths[self.current_image_index])
                    self.set_pic()
        except IndexError:
            # restore current_image_index
            if previous:
                self.current_image_index += 1
            else:
                self.current_image_index -= 1
            pass

        print(self.current_image_index)

    def load_pic(self, img_path):
        self.current_image_filename = os.path.basename(img_path)
        self.current_image_filesize = os.path.getsize(img_path)
        self.current_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        self.current_img = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)

    def reset_pic(self):
        self.set_pic(self.current_img)

    def set_pic(self, img=None):
        if img is None:
            img = self.current_img

        self.pic_real_h, self.pic_real_w = img.shape[:2]

        # adapt window
        monitor_width, monitor_height = self.pic.width(), self.pic.height()
        monitor_ratio = monitor_width / monitor_height
        video_ratio = self.pic_real_w / self.pic_real_h
        # considering calculation precision error issue, don't use "!=" to judge
        if monitor_ratio - video_ratio > 0.1:
            height, width, channel = img.shape
            pile_width = channel * width
            q_image = QImage(img.data, width, height, pile_width, QImage.Format_RGB888)
            qpix = QPixmap.fromImage(q_image).scaled(self.pic.width(), self.pic.height(), Qt.KeepAspectRatio)
        elif monitor_ratio - video_ratio < 0.1:
            height, width, channel = img.shape
            pile_width = channel * width
            q_image = QImage(img.data, width, height, pile_width, QImage.Format_RGB888)
            qpix = QPixmap.fromImage(q_image).scaled(self.pic.width(), self.pic.height(), Qt.KeepAspectRatio)

        self.pic.setPixmap(qpix)

    def draw_on_pic(self):
        cv2.drawMarker(self.current_img_mask, (int(self.pic_real_x), int(self.pic_real_y)), (255, 0, 0),
                       cv2.MARKER_CROSS, 11, 3)

        if len(self.current_points) > 1:
            cv2.line(self.current_img_mask, (self.current_points[-1][0], self.current_points[-1][1]),
                     (self.current_points[-2][0], self.current_points[-2][1]), (0, 255, 0), 3)

        self.set_pic(self.current_img_mask)

    def close_draw(self):
        if len(self.current_points) > 2:
            cv2.line(self.current_img_mask, (self.current_points[-1][0], self.current_points[-1][1]),
                     (self.current_points[0][0], self.current_points[0][1]), (0, 255, 0), 3)

            # summary roi data
            points = np.array(self.current_points)
            min_x = np.min(points[:, 0])
            max_x = np.max(points[:, 0])
            min_y = np.min(points[:, 1])
            max_y = np.max(points[:, 1])

            # cv2.rectangle(self.current_img_mask, (min_x, min_y), (max_x, max_y), (0, 0, 255), 1)
            anchor = (max_x + min_x) / 2, (max_y + min_y) / 2
            self.last_box = [min_x, min_y, max_x - min_x, max_y - min_y, anchor]

            self.set_pic(self.current_img_mask)
            self.old_points = self.current_points

            self.current_points = []

            self.open_for_label = True

    def copy_box(self):
        if len(self.last_box) > 0:
            anchor = self.last_box[4]
            self.new_anchor = self.pic_real_x, self.pic_real_y
            delta = self.new_anchor[0] - anchor[0], self.new_anchor[1] - anchor[1]

            new_points = [(int(p[0] + delta[0]), int(p[1] + delta[1])) for p in self.old_points]

            for i in range(len(new_points) - 1):
                cv2.line(self.current_img_mask, new_points[i], new_points[i + 1], (0, 192, 255), 3)
            cv2.line(self.current_img_mask, new_points[0], new_points[-1], (0, 192, 255), 3)

            # x, y, w, h = self.last_box[0], self.last_box[1], self.last_box[2], self.last_box[3]
            # pt1 = (int(self.pic_real_x - w / 2), int(self.pic_real_y - h / 2))
            # pt2 = (int(self.pic_real_x + w / 2), int(self.pic_real_y + h / 2))
            # cv2.rectangle(self.current_img_mask, pt1, pt2, (0, 128, 255), 1)

            self.set_pic(self.current_img_mask)

    def paintEvent(self, event):
        self.painter = QPainter(self.pic)
        self.painter.begin(self)
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        self.painter.setPen(pen)

        if self.draw == 'point':
            self.painter.drawPoint(self.mouse_window_x, self.mouse_window_y)
        elif self.draw == 'line':
            if len(self.current_points) > 1:
                self.painter.drawLine(self.current_points[-1][0], self.current_points[-1][1],
                                      self.current_points[-2][0], self.current_points[-2][1])

        self.painter.end()

    def check_legal_mouse_co(self):
        if self.pic_real_x >= 0 and self.pic_real_y >= 0:
            return True
        else:
            return False

    def mousePressEvent(self, e):
        if self.check_legal_mouse_co():
            # 左键按下
            if e.buttons() == QtCore.Qt.LeftButton:
                print('左')

                self.current_img_mask = self.current_img.copy()

                if len(self.current_points) == 0:
                    self.current_label = ''
                    self.open_for_label = False

                self.current_points.append([int(self.pic_real_x), int(self.pic_real_y)])
                print(self.current_points)
                self.draw_on_pic()

            # 右键按下
            elif e.buttons() == QtCore.Qt.RightButton:
                print('右')
                # copy box roi
                self.copy_box()

            # 中键按下
            elif e.buttons() == QtCore.Qt.MidButton:
                print('中')

    def mouseDoubleClickEvent(self, e):
        if self.check_legal_mouse_co():
            # 左键双击
            if e.buttons() == QtCore.Qt.LeftButton:
                # self.update()
                print('左双')
                self.close_draw()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.current_points = []
            print(self.current_points, 'clear')
        if self.open_for_label:
            if e.key() in range(48, 58) or e.key() in range(65, 91):
                self.current_label = chr(e.key())
                self.write_to_json()
                self.open_for_label = False

    def write_to_json(self):
        # write to JSON
        self.il_buf.add_serial(self.current_image_filename, self.current_image_filesize,
                               region_points=self.old_points, obj_name=self.current_label)

        x, y = self.last_box[0], self.last_box[1]
        cv2.putText(self.current_img_mask, self.current_label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        self.set_pic(self.current_img_mask)

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

    def load_img(self):
        self.image_paths = self.file_select_dialog('选择图片')
        self.image_paths = self.image_paths[0]

        # load the first image
        self.load_pic(self.image_paths[0])
        self.set_pic()

    def load_json(self):
        self.json_paths = self.file_select_dialog('要载入的图片标注数据', filter='JSON Files (*.json)')
        self.json_paths = self.image_paths[0]

        self.il = ImageLabels(self.json_paths)

    def save_json(self):
        json_data_output = json.dumps(self.il_buf.json_data, ensure_ascii=False).encode()

        json_save_path = self.file_select_dialog('要保存的图片标注数据', filter='JSON Files (*.json)', save=True)[0]
        f = open(json_save_path, 'wb')
        f.write(json_data_output)
        f.close()

    def file_select_dialog(self, dialog_name, path_select=False, default_path=None, filter="Image Files (*.jpg)",
                           save=False):
        # filter_str = filter
        # file_path, current_filter = QFileDialog.getOpenFileNames(self, dialog_name, default_path, "Text Files (*.txt);;All Files (*)")
        if not path_select:
            if not save:
                file_path, current_filter = QFileDialog.getOpenFileNames(self, dialog_name, default_path,
                                                                         filter)
            else:
                file_path, current_filter = QFileDialog.getSaveFileName(self, dialog_name, default_path, filter=filter)

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

        if mouse_x != self.old_x or mouse_y != self.old_y:
            if pic_x < mouse_x < pic_w + pic_x and pic_y < mouse_y < pic_h + pic_y:
                self.old_x = mouse_x
                self.old_y = mouse_y

                monitor_x = mouse_x - pic_x
                monitor_y = mouse_y - pic_y

                monitor_x *= mainWindow.pic_real_w / pic_w
                monitor_y *= mainWindow.pic_real_h / pic_h

                mainWindow.pic_real_x = monitor_x
                mainWindow.pic_real_y = monitor_y

                # print(monitor_x, monitor_y)
            else:
                mainWindow.pic_real_x = -1
                mainWindow.pic_real_y = -1


# setup GUI
app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()

sys.exit(app.exec_())
