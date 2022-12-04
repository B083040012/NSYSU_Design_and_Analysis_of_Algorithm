"""
Voronoi Diagram (Divide and Conquer) 
Course: Design and Analysis of Algorithm, 2022 Fall, NSYSU
Author: Bo Han, Chen
Student ID: B083040012
"""

from PyQt5 import QtWidgets

from voronoi_controller import MainWindowController

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindowController()
    window.show()
    sys.exit(app.exec_())