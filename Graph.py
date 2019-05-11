# -*- coding: utf-8 -*-
# -*- coding: 850 -*-

import datetime

from PyQt5.QtCore import QTime
import pyqtgraph as pg

import pytz

UNIX_EPOCH_naive = datetime.datetime(1970, 1, 1, 0, 0) #offset-naive datetime
UNIX_EPOCH_offset_aware = datetime.datetime(1970, 1, 1, 0, 0, tzinfo = pytz.utc) #offset-aware datetime
UNIX_EPOCH = UNIX_EPOCH_naive

TS_MULT_us = 1e6

def now_timestamp(ts_mult=TS_MULT_us, epoch=UNIX_EPOCH):
    return(int((datetime.datetime.utcnow() - epoch).total_seconds()*ts_mult))

def int2dt(ts, ts_mult=TS_MULT_us):
    return(datetime.datetime.utcfromtimestamp(float(ts)/ts_mult))

def dt2int(dt, ts_mult=TS_MULT_us, epoch=UNIX_EPOCH):
    delta = dt - epoch
    return(int(delta.total_seconds()*ts_mult))

def td2int(td, ts_mult=TS_MULT_us):
    return(int(td.total_seconds()*ts_mult))

def int2td(ts, ts_mult=TS_MULT_us):
    return(datetime.timedelta(seconds=float(ts)/ts_mult))

class  TimeAxisItem(pg.AxisItem):


    def __init__(self, *args, **kwargs):
        super(TimeAxisItem, self).__init__(*args, **kwargs)


    def tickStrings(self, values, scale, spacing):
        return [int2dt(value).strftime("%M:%S.%f") for value in values]

class  Trend(pg.GraphicsWindow):

    def __init__(self, parent=None, **kargs):

        pg.GraphicsWindow.__init__(self, **kargs)
        self.setParent(parent)

        pg.setConfigOption('background', [0, 0, 0, ])
        pg.setConfigOption('foreground', 'w')

        self.t = QTime()
        self.t.start()

        self.plots_enabled = []
        self.plot_list = []
        self.pen_plots = []

        testBenchPlot = self.addPlot(row=0,col=0,labels =  {'left': 'Test Bench', 'bottom': 't'}, axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        testBenchPlot.showGrid(x=True, y=True)

        self.data_t = []
        self.data0 = []

        self.pt1_press = testBenchPlot.plot()
        self.pt2_press = testBenchPlot.plot()
        self.p1_press = testBenchPlot.plot()

        self.pt1_flow = testBenchPlot.plot()
        self.pt2_flow = testBenchPlot.plot()
        self.p1_flow = testBenchPlot.plot()
        self.speed_shaft = testBenchPlot.plot()
        self.torque_shaft = testBenchPlot.plot()

        self.temp = testBenchPlot.plot()

        self.plot_list.append(self.pt1_press)  # index 0
        self.plot_list.append(self.pt1_flow)
        self.plot_list.append(self.temp)
        self.plot_list.append(self.speed_shaft)
        self.plot_list.append(self.pt2_press)
        self.plot_list.append(self.pt2_flow)
        self.plot_list.append(self.p1_press)
        self.plot_list.append(self.p1_flow)
        self.plot_list.append(self.torque_shaft)  # index 8



        if self.pen_plots != None:
            self.update_pens()

    def update_live_data(self, d):
        self.data_t.append(now_timestamp())
        self.data0.append(d)
        self.update_plots()

    def update_rec_data(self, d):
        self.data_t.append(d.pop())
        self.data0.append(d)
        self.update_plots()

    def set_on_plots(self, l):
        self.plots_enabled = l

    def update_plots(self):
        for i in self.plots_enabled.buttons():
            if i.isChecked():
                self.plot_list[self.plots_enabled.id(i)]\
                    .setData(x=list(self.data_t),
                             y=list([item[self.plots_enabled.id(i)] for item in self.data0]))

    def set_pen_colors(self, l):
        self.pen_plots = l
        self.update_pens()

    def update_pens(self):
        for i in range(len(self.pen_plots)):
            self.plot_list[i].setPen(self.pen_plots[i])