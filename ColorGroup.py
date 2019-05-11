from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal


class QColorGroup(QtCore.QObject):

    colorList = pyqtSignal(list)
    color_list = []
    g = QtWidgets.QButtonGroup()
    m = 0

    def addButton(self, button):
        self.g.addButton(button, self.m)
        self.g.setExclusive(False)
        self.color_list.append(button._color)
        button.colorChanged.connect(self.color_changed)

    def removeButton(self, button):
        button.colorChanged.disconnect()

    def color_changed(self):
        i = 0
        for n in self.g.buttons():
            if self.color_list[i] != n._color:
                self.color_list[i] = n._color
            i += 1
        self.colorList.emit(self.color_list)

