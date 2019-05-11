#!/usr/bin/python

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSignal


class QTable(QtWidgets.QTableWidget):

    signal = pyqtSignal()

    def __init__(self, *args):
        super(QTable, self).__init__(*args)

        self._factor = 0
        self._header = []
        self._target_items = []
        self.samples_table = []

        self._selector = QtWidgets.QComboBox()
        self._selector.addItems(["P1", "PT1", "PT2"])

        self._flow_item = QtWidgets.QDoubleSpinBox()
        self._flow_item.setMaximum(50)
        self._flow_item.setDecimals(1)
        self._flow_item.setReadOnly(True)
        self._flow_item.setAlignment(Qt.AlignCenter)
        self._flow_item.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        self._press_item = QtWidgets.QDoubleSpinBox()
        self._press_item.setMaximum(500)
        if self._factor < 1:
            self._press_item.setDecimals(0)
        else:
            self._press_item.setDecimals(1)
        self._press_item.setAlignment(Qt.AlignCenter)
        self._press_item.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

    def set_header(self, h):
        self._header = h

    def set_target_items(self, t):
        self._target_items = t
        self.update_values()

    def config_table(self):
        self.setColumnCount(len(self._header))
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.resizeColumnsToContents()
        for i in range(self.columnCount()):
            _item = QtWidgets.QTableWidgetItem(self._header[i])
            self.setHorizontalHeaderItem(i, _item)
        self.insertRow(self.rowCount())
        self.set_row_items()

    def get_sample(self):
        _sample = []
        _row = self.rowCount()-1
        _item = self._selector.currentText()
        _item = QtWidgets.QTableWidgetItem(_item)
        self.setItem(_row, 0, _item)

        _item = self._press_item.value()
        _sample.append(_item)
        _item = str(_item)
        _item = QtWidgets.QTableWidgetItem(_item)
        self.setItem(_row, 1, _item)

        _item = self._flow_item.value()
        _sample.append(_item)
        _item = str(_item)
        _item = QtWidgets.QTableWidgetItem(_item)
        self.setItem(_row, 2, _item)
        self.insertRow(self.rowCount())
        self.set_row_items()
        self.fill_sample_table(_sample)

    def set_row_items(self):
        self.setCellWidget(self.rowCount()-1, 0, self._selector)
        self.setCellWidget(self.rowCount()-1, 1, self._press_item)
        self.setCellWidget(self.rowCount()-1, 2, self._flow_item)

    def delete_table(self):

        if self.rowCount() > 1:
            self.removeRow(self.rowAt(self.rowCount()-1))
            self.samples_table.pop(-1)

    def update_values(self):
        self._press_item.setValue(self._target_items[self._selector.currentIndex()][0])
        self._flow_item.setValue(self._target_items[self._selector.currentIndex()][1])

    def fill_sample_table(self, sample):
        self.samples_table.append(sample)
        print self.samples_table