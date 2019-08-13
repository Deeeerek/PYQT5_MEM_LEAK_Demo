# coding=utf-8
# -*- coding: utf-8 -*-
import sys
import gc
import objgraph
import matplotlib

import pandas as pd
import os
from demo import Ui_Form as Ui_Form
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import *
from memory_profiler import profile


progname = os.path.basename(sys.argv[0])
progversion = "0.1"

global counter,glb_case_list,pb_waveform_switch,xdata, ydata,Pre_MainTabIndex
n_drops = 100

xdata, ydata = [], []
counter=0
pb_waveform_switch=True


class MyMplCanvas(FigureCanvas):
    __slots__ = ('axes', 'figure')
    def __init__(self, width, height, dpi):
        # 创建一个Figure,该Figure为matplotlib下的Figure，不是matplotlib.pyplot下面的Figure
        self.fig = Figure(figsize=(QSizePolicy.Expanding, QSizePolicy.Expanding), dpi=dpi)
        # 在父类中激活Figure窗口，此句必不可少，否则不能显示图形
        super(MyMplCanvas, self).__init__(self.fig)
        # 调用Figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot(1,1,1)方法
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlim(0, 110)
        self.axes.set_ylim(0, 300)
        self.axes.set_xticks(np.arange(20,110,20))
        self.axes.set_xlabel('time(s)')
        self.axes.set_ylabel('Currnt(A)')
        ylimHi = 20
        ylimLow = 0
        self.axes.set_ylim(ylimLow, ylimHi)
        del ylimHi,ylimLow
        self.axes.set_xlabel('time(s)')
        self.axes.set_ylabel('Currnt(A)')

        self.axes.grid(True)



class Mainwindow(QWidget, Ui_Form):
    def __init__(self):
        super(Mainwindow,self).__init__()
        self.setupUi(self)
        self.Waveform_fig = MyMplCanvas(width=QSizePolicy.Expanding, height=QSizePolicy.Expanding, dpi=100)
        self.gridlayout = QGridLayout(self.frame)
        self.gridlayout.addWidget(self.Waveform_fig)

        # ===================================================================================== #
        # ==========================         Slot & Signal           ========================== #
        # ===================================================================================== #
        self.pushButton.clicked.connect(self.On_Plot_waveform)

        # New thread for power update, interval time = 200ms
        # self.PowerUpdateTriggerThread = PowerUpdateTrigger()
        # self.PowerUpdateThread = PowerUpdate()
        # self.PowerUpdateTriggerThread.Trigger.connect(self.On_PowerUpdate)
        # self.PowerUpdateThread.UpdateData.connect(self.Data_collection)


    def On_Plot_waveform(self):


        global pb_waveform_switch
        global xdata, ydata, counter
        xdata, ydata = [], []
        counter = 0
        if pb_waveform_switch==True:

            self.b=list(range(0, 110))
            # print(self.b)
            # print(self.cb_waveform_select.currentIndex())

            self.ani = FuncAnimation(self.Waveform_fig.figure, self.On_UpdateWaveform,frames=19, blit=True, \
                                     interval=100,cache_frame_data=False,save_count=0)


            self.pushButton.setText('Pause')
            pb_waveform_switch=False

        else:
            self.ani.event_source.stop()
            self.pushButton.setText('Start')
            pb_waveform_switch=True

    @profile()
    def On_UpdateWaveform(self,frames):
        global xdata, ydata,counter
        # dummy data
        MeanVal = list(range(0,24))

        Index=15
        templist=[]
        templist.append(MeanVal[Index])

        if  counter <= 110:

            xdata.append(counter)
            ydata.append(templist[-1])
        else:
            del ydata[0]
            ydata.append(templist[-1])

        lin=self.Waveform_fig.axes.plot(xdata, ydata, 'r-', animated=False)

        if counter>300:
            counter=counter-150

        counter=counter+1

        del MeanVal,templist

        gc.collect()
        return lin



    def get_size(self,obj, seen=None):
        # From
        # Recursively finds size of objects
        size = sys.getsizeof(obj)
        if seen is None:
            seen = set()
        obj_id = id(obj)
        if obj_id in seen:
            return 0
    # Important mark as seen *before* entering recursion to gracefully handle
        # self-referential objects
        seen.add(obj_id)
        if isinstance(obj, dict):
          size += sum([sys.get_size(v, seen) for v in obj.values()])
          size += sum([sys.get_size(k, seen) for k in obj.keys()])
        elif hasattr(obj, '__dict__'):
          size += sys.get_size(obj.__dict__, seen)
        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
          size += sum([sys.get_size(i, seen) for i in obj])
        return size

if __name__ == '__main__':

    gc.enable()


    app = QApplication(sys.argv)
    main = Mainwindow()

    main.show()
    sys.exit(app.exec_())
