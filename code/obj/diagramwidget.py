"""
Voronoi Diagram (Divide and Conquer) 
Course: Design and Analysis of Algorithm, 2022 Fall, NSYSU
Author: Bo Han, Chen
Student ID: B083040012
"""

from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class diagramWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

    def reset(self):
        self.canvas.axes.clear()
        self.canvas.axes.set_xlim([0, 600])
        self.canvas.axes.set_ylim([0, 600])
        self.canvas.axes.invert_yaxis()
        self.canvas.draw()