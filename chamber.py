
from __future__ import unicode_literals

from numpy import arange, sin, pi
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import a
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtWidgets
import torch
from torchvision import utils as vutils

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class Oracle():
    # for visualization
    def __init__(self):
        pass

    def visualize_tensors(self, tensor_list, file="./sandbox_results/temp"):

        # Visualize Variable list (concatenating vertically) and save them in a file
        # accepts a list of Variables of the form batch x * x (size1 x size2)

        cmax = -1
        proper_size = None

        t_vis = []
        for tensor in tensor_list:
            t_size = tensor.size()[1]
            if cmax < t_size:
                cmax = t_size
            proper_size = tensor.size()

        for tensor in tensor_list:
            if tensor.size()[1] < cmax:
                t_vis.append(tensor.expand((proper_size[0], cmax, proper_size[2], proper_size[3])))
            else:
                t_vis.append(tensor)

        vis = torch.cat(t_vis, 0)

        if "png" not in file:
            file += ".png"

        vutils.save_image(vis,file, nrow=proper_size[0], pad_value=1.0, normalize=False)

class Historian():
    # for logging
    def __init__(self):
        pass

class Chamber(QMainWindow):
    def rec_print(self,a):
        for c in a.children():
            self.rec_print(c)
            print(a.objectName())

    def __init__(self):
        super().__init__()

        main = uic.loadUi("core.ui",self)
        print(main)
        self.main_widget = QtWidgets.QWidget(main)

        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)

        print(main.verticalLayout)

        main.verticalLayout.addWidget(dc)


        self.show()

