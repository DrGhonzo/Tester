#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: 850 -*-

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from pyModbusTCP.client import ModbusClient
import csv
import time
import Queue
import sys

from _test_bench import Ui_MainWindow
from tables import Test_Report


class CommEngine(QThread):
    measurements_signals = pyqtSignal(list, name='m_signals')
    state_signals = pyqtSignal(str, name='st_signals')

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        self.state_signals.emit("Running")
        SERVER_HOST = "192.168.2.30"
        SERVER_PORT = 502

        # TCP auto connect on modbus request, close after it
        c = ModbusClient()

        # uncomment this line to see debug message
        # c.debug(True)

        # define modbus server host, port
        c.host(SERVER_HOST)
        c.port(SERVER_PORT)

        while True:
            # open or reconnect TCP to server
            if not c.is_open():
                if not c.open():
                    self.state_signals.emit("Unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

            if c.is_open():

                reads = c.read_holding_registers(0, 9)

                self.state_signals.emit("Connected to " + SERVER_HOST + ":" + str(SERVER_PORT))
                # if success display registers
                if reads:
                    # self.pressure_signals.emit(CustomW.slot_print(press))
                    self.state_signals.emit("Incoming data")
                    self.measurements_signals.emit(reads)
                    q.put(reads)

            time.sleep(0.1)
            c.close()

    def stop(self):
        if self.isRunning():
            self.terminate()
            self.state_signals.emit("Stop")


class RecordEngine(QThread):
    state_signals = pyqtSignal(str, name='st_signals')

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        self.state_signals.emit("grabando")
        fname = ui.date_edit.date()
        fname = fname.toPyDate()
        fname = str(fname)
        fname = fname + "-" + ui.customer_lineEdit.text() + "-" + ui.wo_lineEdit.text()
        f.put(fname)

        header = []
        with open(fname + ".csv", 'a') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
        file.close()

        while True:
            p = q.get()
            p.append(time.strftime("%H:%M:%S"))
            with open(fname + ".csv", 'a') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(p)
                time.sleep(0.5)

    def stop(self):
        if self.isRunning():
            self.terminate()
            self.state_signals.emit("Stop")


def populate_data_table(p):
    _data = [str(i) for i in p]
    _data.append(time.strftime("%H:%M:%S"))
    _data.append(time.strftime("%m/%d/%y"))
    ui.data_table_widget.insertRow(ui.data_table_widget.rowCount())
    for i in range(len(_data)):
        _item = QtWidgets.QTableWidgetItem(_data[i])
        _item.setTextAlignment(Qt.AlignCenter)
        ui.data_table_widget.setItem(ui.data_table_widget.rowCount()-1, i, _item)
        # ui.data_table_widget.resizeColumnsToContents()


def live_values(p):
    for i in range(len(p)):
        if i == 2:
            ui.panel_value_list[i].setValue(p[i])
            ui.graph_value_list[i].setValue(p[i])
            ui.gauge_list[i].update_value(p[i])
            ui.test_current_temp_spinBox.setValue((p[i]))
        else:
            ui.panel_value_list[i].setValue(p[i])
            ui.graph_value_list[i].setValue(p[i])
            ui.gauge_list[i].update_value(p[i])
    _target_items = [[p[6], p[7]], [p[0], p[1]], [p[4], p[5]]]
    if ui.units_combo.currentIndex() == 0:
        ui.imperial_report_table.set_target_items(_target_items)
    else:
        ui.metric_report_table.set_target_items(_target_items)


def update_plots():
    ui.graph_widget.set_on_plots(ui.enablePlotsGroup)


def create_report():
    data = []
    report_engine.run()

    data.append(ui.make_lineEdit.text())
    data.append(ui.model_lineEdit.text())
    data.append(ui.test_current_temp_spinBox.value())
    data.append(ui.test_speed_spinBox.value())
    data.append(ui.test_duration_spinBox.value())
    data.append(ui.test_rotation_combo.currentText())
    data.append(ui.test_peak_press_spinBox.value())
    data.append(ui.test_units_lbl.text())
    data.append(ui.test_cycles_spinBox.value())

    report_engine.fill_test_table(data)
    report_engine.fill_sample_table(ui.imperial_report_table.samples_table)

    fname = ui.date_edit.date()
    fname = fname.toPyDate()
    fname = str(fname)
    fname = fname + "-" + ui.customer_lineEdit.text() + "-" + ui.wo_lineEdit.text()

    report_engine.update(fname + ".pdf")
    report_engine.build()



if __name__ == "__main__":

    f = Queue.Queue()
    q = Queue.Queue()

    # ----------create GUI to show data, graph and controls the app
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    com_engine = CommEngine()
    com_engine.measurements_signals.connect(ui.graph_widget.update_live_data)
    com_engine.measurements_signals.connect(live_values)
    com_engine.measurements_signals.connect(populate_data_table)

    record_engine = RecordEngine()
    ui.controls_start_bttn.clicked[bool].connect(lambda: com_engine.start())
    ui.controls_stop_bttn.clicked[bool].connect(lambda: com_engine.stop())

    report_engine = Test_Report()
    ui.controls_report_bttn.clicked[bool].connect(lambda: create_report())

    ui.graph_widget.set_on_plots(ui.enablePlotsGroup)
    ui.enablePlotsGroup.buttonClicked.connect(update_plots)

    ui.graph_widget.set_pen_colors(ui.colorGroup.color_list)
    ui.colorGroup.colorList.connect(ui.graph_widget.set_pen_colors)

    app.aboutToQuit.connect(com_engine.stop)

    sys.exit(app.exec_())


