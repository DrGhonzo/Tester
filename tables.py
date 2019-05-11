# -*- coding: utf-8 -*-
# -*- coding: 850 -*-

from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet
from PyQt5.QtCore import QThread


class Test_Report(QThread):
    def __init__(self):
        QThread.__init__(self)


    def run(self):
        self.elements = []

        styleSheet = getSampleStyleSheet()

        self.I = Image('/home/luciano/Escritorio/Trabajos/Drive Train Services/HMI/drive_train_logo.png',
                       width=120, height=40)
        self.I.hAlign = 'RIGHT'

        self.MainTitle = Paragraph('''<para alignment=center><b>HIDRAULIC PUMP TEST RESULT</b></para>''',
                                   styleSheet["Heading1"])

        self.CompanyBrief = Paragraph('''<para alignment=justify><b>Thank you for doing busines with us.
         We have individually tested this product
         to meet or exceed the O.E.M. specifications to ensure exceptional quality and performance</b></para>''',
                                      styleSheet["Heading4"])

        self.SpecialNotes = Paragraph('''<b>Special Notes</b>''', styleSheet["Heading4"])

        self.Instructions = Paragraph('''<para alignment=center><b>*** Start up instructions *** 
        to help prevent pump damage</b></para>''', styleSheet['BodyText'])
        self.Instructions.hAlign = 'CENTER'

        _point_1 = Paragraph('Use oil with the proper viscosity at operating temperature',
                             styleSheet['BodyText'], bulletText='>')
        _point_2 = Paragraph('Fill the pump at least half full with filtered hydraulic fluid before start up',
                             styleSheet['BodyText'], bulletText='>')
        _point_3 = Paragraph('use an air bleed valve if the circuit has blocked flow on start up',
                             styleSheet['BodyText'], bulletText='>')
        _point_4 = Paragraph('use check valve in line service to prevent pump reversal',
                             styleSheet['BodyText'], bulletText='>')
        _point_5 = Paragraph('Do not press coupling halves tightly together!'
                             ' Allow clearance between hub and insert to prevent end of thrust into pump shaft',
                             styleSheet['BodyText'], bulletText='>')

        self.Instruction_list = [_point_1, _point_2, _point_3, _point_4, _point_5]

        self.Final_Setting = Paragraph('''<para alignment=justify><i>This unit's control has a final setting 
        of "nanu nanu" for shipment.</i></para>''',
                                       styleSheet['BodyText'])
        self.StandBy_Setting = Paragraph('''<para alignment=justify><i>This unit's control stand by pressure is set at 
        "nanu nanu" for shipment.</i></para>''',
                                         styleSheet['BodyText'])
        self.Date_report = Paragraph('''<para alignment=left><b>THIS TEST REPORT COMPLETE ON</b></para>''',
                                     styleSheet['BodyText'])

        self.t_2 = [['Test Pressure', 'Pump Flow']]

    def fill_test_table(self, _data):
        row_0 = ['Brand:', _data[0], 'Model Code:', _data[1]]
        row_1 = ['Oil Temp:', str(_data[2]), '°F', 'Rotation:', _data[5]]
        row_2 = ['Test Speed:', str(_data[3]), 'RPM', 'Peak Test\nPressure:', str(_data[6]), _data[7]]
        row_3 = ['Test Duration:', str(_data[4]), 'min', 'Test Cycles:', str(_data[8])]

        self.t_1 = [row_0, row_1, row_2, row_3]

        self.table_1 = Table(self.t_1, colWidths=80, style=[('GRID', (0, 0), (-1, -1), 0.5, colors.white),
                                                       ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                                                       ('BACKGROUND', (3, 1), (3, 3), colors.lightgrey),
                                                       ('BACKGROUND', (2, 0), (2, 0), colors.lightgrey),
                                                       ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                                                       ('ALIGN', (2, 1), (2, 3), 'LEFT'),
                                                       ('ALIGN', (-1, 2), (-1, 2), 'LEFT')])

    def fill_sample_table(self, _list): # read a list of lists with shape [n-sample][pressure,flow]
        for sample in _list:
            self.t_2.append([sample[0], sample[1]])

        self.table_2 = Table(self.t_2, colWidths=80, style=[('GRID', (0, 0), (-1, -1), 0.5, colors.white),
                                                       ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey)])

        self.table_3 = Table(self.t_2, colWidths=80, style=[('GRID', (0, 0), (-1, -1), 0.5, colors.white),
                                                       ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey)])

    def update(self, filename):
        self.doc = SimpleDocTemplate(filename, pagesize=A4)

        self.elements.append(self.I)
        self.elements.append(Spacer(200, 10))
        self.elements.append(self.MainTitle)
        self.elements.append(self.CompanyBrief)
        self.elements.append(Spacer(200, 10))
        self.elements.append(self.table_1)
        self.elements.append(Spacer(200, 10))
        self.elements.append(self.table_2)
        self.elements.append(Spacer(200, 10))
        self.elements.append(self.table_3)
        self.elements.append(Spacer(200, 8))
        self.elements.append(self.SpecialNotes)
        self.elements.append(Spacer(200, 8))
        self.elements.append(self.Instructions)
        self.elements.extend(self.Instruction_list)
        self.elements.append(Spacer(200, 8))
        self.elements.append(self.Final_Setting)
        self.elements.append(self.StandBy_Setting)
        self.elements.append(Spacer(200, 8))
        self.elements.append(self.Date_report)

    def build(self):
        self.doc.build(self.elements)
        if self.isRunning():
            self.stop()