# -*- coding: utf-8 -*-

"""
Py40 PyQt5 tutorial

This program centers a window
on the screen.

author: QiuChen
last edited: 12 2017
"""

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.resize(100, 100)
        self.center()
        #lbl1 = QLabel('+', self)
        #lbl1.move(15, 10)
        self.setWindowFlags(Qt.WindowStaysOnTopHint|\
                            Qt.SplashScreen|\
                            Qt.FramelessWindowHint)
        #self.setWindowOpacity(0.5)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show()


    #控制窗口显示在屏幕中心的方法
    def center(self):

        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.red, 1, Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(40, 70, 60, 70)
        qp.drawLine(50, 60, 50, 80)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())