# coding=utf-8
# -*- coding: utf-8 -*-
import sys
import gc
import objgraph
import matplotlib
from demo import Ui_Form as Ui_Form
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
import os
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from memory_profiler import profile


progname = os.path.basename(sys.argv[0])
progversion = "0.1"

global counter,glb_case_list,pb_waveform_switch,xdata, ydata,Pre_MainTabIndex
n_drops = 100

xdata, ydata = [], []
counter=0
pb_waveform_switch=True

# print(matplotlib.get_backend())

class PowerUpdateTrigger(QThread):
    Trigger = pyqtSignal() # customized signal, no var
    def __init__(self, parent=None):
        super(PowerUpdateTrigger, self).__init__(parent)
        self.working = True
        self.num = 0
    def __del__(self):
        self.working = False
        self.wait()


    def run(self):
        while self.working == True:
            self.Trigger.emit()
            self.msleep(200)



class PowerUpdate(QThread):
    UpdateData = pyqtSignal() # customized signal, pd.DataFrame
    def __init__(self, parent=None):
        super(PowerUpdate, self).__init__(parent)

    @profile
    def run(self):
        ReadVal_pd=None
        start = time.clock()
        self.msleep(100)

        end = time.clock()
        t=end-start
        # self.deleteLater()
        print("Runtime is ：",t)


class Mainwindow(QWidget, Ui_Form):
    def __init__(self):
        super(Mainwindow,self).__init__()
        self.setupUi(self)


        # ===================================================================================== #
        # ==========================         Slot & Signal           ========================== #
        # ===================================================================================== #
        # New thread for power update, interval time = 200ms
        self.PowerUpdateTriggerThread = PowerUpdateTrigger()
        self.PowerUpdateThread = PowerUpdate()
        self.PowerUpdateTriggerThread.Trigger.connect(self.On_PowerUpdate)
        self.PowerUpdateThread.UpdateData.connect(self.Data_collection)
        self.PowerUpdateTriggerThread.start()

    @profile
    def On_PowerUpdate(self):
        # self.PowerUpdateThread.working=True
        self.PowerUpdateThread.start()
        # objgraph.show_most_common_types(100)

    @profile
    def Data_collection(self):
        pass
        # prod = [round((a - b) * c, 3) for a, b, c in zip(MeanVal, self.OffsetList, self.GainList)]
        # del prod
        # gc.collect()

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
