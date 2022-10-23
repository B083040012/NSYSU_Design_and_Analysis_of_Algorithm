from PIL import ImageQt, Image
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel
from PyQt5.QtCore import QEvent
from matplotlib.backend_bases import MouseButton
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

from voronoi_GUI import Ui_MainWindow
from my_voronoi import myVoronoiDiagram

class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
    
    def setup_control(self):
        # tool bar of matplotlib
        # self.addToolBar(NavigationToolbar(self.ui.diagram_widget.canvas, self))
        # connect the matplotlib to the event method
        self.ui.diagram_widget.canvas.mpl_connect("motion_notify_event", self.diagram_move)
        self.ui.diagram_widget.canvas.mpl_connect("button_press_event", self.diagram_press)
        self.ui.diagram_widget.canvas.axes.set_xlim([0, 600])
        self.ui.diagram_widget.canvas.axes.set_ylim([0, 600])

        self.ui.actionOpenPoint.triggered.connect(lambda: self.open_file("point"))
        self.ui.actionOpenDiagram.triggered.connect(lambda: self.open_file("diagram"))
        self.ui.actionReset.triggered.connect(lambda: self.reset())
        self.ui.next_case_Button.clicked.connect(lambda: self.next_case())
        self.ui.next_step_Button.clicked.connect(lambda: self.next_step())

        self.vonoroi = myVoronoiDiagram()
        self.plot_point()

    def diagram_move(self, event):
        x = int(event.xdata) if event.xdata != None else None
        y = int(event.ydata) if event.ydata != None else None
        inaxes = event.inaxes
        self.ui.statusbar.showMessage(("x = {0}, y = {1}, axes = {2}".format(x, y, inaxes)))

    def diagram_press(self, event):
        x = int(event.xdata) if event.xdata != None else None
        y = int(event.ydata) if event.ydata != None else None
        if x is None or y is None:
            print("invalid coordinate!!")
        else:
            print("add point on x = {0}, y = {1}".format(x, y))
            self.plot_point(x, y)

    def plot_point(self, x = None, y = None):
        # x_list = [float(i) for i in range(0, x_axis_max+1, 100)]
        # y_list = [float(i) for i in range(0, y_axis_max+1, 100)]
        # self.ui.diagram_widget.canvas.axes.clear()
        if x is not None and y is not None:
            self.ui.diagram_widget.canvas.axes.set_xlim([0, 600])
            self.ui.diagram_widget.canvas.axes.set_ylim([0, 600])
            self.ui.diagram_widget.canvas.axes.scatter(x, y)
        self.ui.diagram_widget.canvas.draw()

    def plot_diagram(self, ele_list):
        for i in range(0, len(ele_list[1][0][0])):
            tmp_x = [ele_list[1][0][0][i], ele_list[1][1][0][i]]
            tmp_y = [ele_list[1][0][1][i], ele_list[1][1][1][i]]
            self.ui.diagram_widget.canvas.axes.plot(tmp_x, tmp_y)
        self.ui.diagram_widget.canvas.draw()

    def open_file(self, type):
        filename, filetype = QFileDialog.getOpenFileName(self, "Open File", './test_data')
        if type == "point":
            self.vonoroi.read_file(filename, type)
            if len(self.vonoroi.test_case_list) <= 0:
                return -1
            self.ui.diagram_widget.canvas.axes.clear()
            self.ui.messageLabel.setText("Please press next case button")
        elif type == "diagram":
            tmp_voronoi = myVoronoiDiagram()
            tmp_voronoi.read_file(filename, type)
            self.ui.diagram_widget.canvas.axes.clear()
            self.plot_point(tmp_voronoi.diagram_ele_list[0][0], tmp_voronoi.diagram_ele_list[0][1])
            self.plot_diagram(tmp_voronoi.diagram_ele_list)

    def open_diagram_file(self):
        # filename, filetype = QFileDialog.getOpenFileName(self, "Open File", './test_data')
        # self.
        pass

    def next_case(self):
        x_list, y_list = self.vonoroi.next_case()
        if x_list == -1 or y_list == -1:
            self.ui.messageLabel.setText("End of test")
            return
        coor_info = ""
        for i in range(0, len(self.vonoroi.current_case[0])):
            coor_info += "({0}, {1})".format(self.vonoroi.current_case[0][i], self.vonoroi.current_case[1][i])
            if i%3 == 2:
                coor_info += "\n"
            else:
                coor_info += " "
        self.ui.messageLabel.setText("Test case: {0}\ntest coordinate:\n{1}".format(self.vonoroi.current_case_index, coor_info))
        self.ui.diagram_widget.canvas.axes.clear()
        self.plot_point(x = x_list, y = y_list)