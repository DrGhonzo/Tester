#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, pyqtSignal


class BurningWidget(QtWidgets.QWidget):

    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(BurningWidget, self).__init__(parent)

        self.use_timer_event = False

        self.value = 35
        self.steps = 10
        self.span = 210
        self.zero = 0
        self.range = 0
        self.zones = []
        self.num = []

        self.set_range(self.zero, self.span)
        self.set_nums()

        if self.use_timer_event:
            timer = QTimer(self)
            timer.timeout.connect(self.update)
            timer.start(5)
        else:
            self.update()

    def set_steps(self, steps):
        self.steps = steps

    def set_span(self, span):
        self.span = span

    def set_zero(self, zero):
        self.zero = zero

    def set_range(self, zero, span):
        self.range = span - zero
        self.zero = zero
        self.span = span

    def set_nums(self):
        stp = (self.span - self.zero)/self.steps
        for i in range(self.steps):
            self.num.append(i * stp)

    def add_zone(self, zone, color):
        aux = int((zone * self.span)/100)
        self.zones.append([aux, color])

    def set_zones(self, h):
        self.zones.sort(reverse=True, key=lambda x: x[0])
        for step in range(len(self.zones)):
            aux = (int((h / self.span) * self.zones[step][0]))
            self.zones[step][0] = aux

    def update_value(self, value):

        if value <= self.zero:
            self.value = self.zero
        elif value >= self.span:
            self.value = self.span
        else:
            self.value = value
        # self.paintEvent("")
        self.valueChanged.emit(int(value))
        # print(self.value)

        # ohne timer: aktiviere self.update()
        if not self.use_timer_event:
            self.update()

    def paintEvent(self, event):

        self.drawWidget()
        self.draw_cursor()
        self.create_value_scale()

    def draw_cursor(self):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        w = self.width()
        h = self.height()
        cursor = int((h / self.span) * self.value)
        cursor = h - cursor
        pen = QtGui.QPen(QtGui.QColor('grey'), 2,
                         QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(int(w * 0.5) + 1, cursor, int(w * 0.5) - 4, 4)
        '''painter.setPen(pen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRoundedRect(w - 4, cursor, 2, h - 1, 1.8, 1.8)'''
        painter.setPen(QtGui.QColor('white'))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(int(w * 0.5) + 2, cursor + 1, int(w * 0.5) - 6, 1)


    def drawWidget(self, ):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        self.set_zones(h)

        for gap in range(len(self.zones)):
            painter.setPen(QtGui.QColor(self.zones[gap][1]))
            painter.setBrush(QtGui.QColor(self.zones[gap][1]))
            painter.drawRoundedRect(int(w * 0.5), (h-self.zones[gap][0]), int(w * 0.5), h, 1.8, 1.8)

        pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 1,
                         QtCore.Qt.SolidLine)

        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRoundedRect(int(w * 0.5), 0, int(w * 0.5) - 1, h - 1, 1.8, 1.8)

    def create_value_scale(self):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        painter.setPen(QtGui.QColor(0, 0, 0))
        font = QtGui.QFont('Noto Sans', 8, QtGui.QFont.Light)
        painter.setFont(font)
        step = int(round(h / self.steps))

        j = -1

        for i in range(step, self.steps * step, step):
            painter.drawLine(int(w * 0.5) - 5, i, int(w * 0.5) + 5, i)
            metrics = painter.fontMetrics()
            fw = metrics.width(str(self.num[j]))
            if self.num[j] < 100:
                painter.drawText((fw / 2) - 2, i, str(self.num[j]))
            else:
                painter.drawText((fw / 2) - 10, i, str(self.num[j]))
            j = j - 1