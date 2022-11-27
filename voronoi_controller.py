from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

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
        self.ui.diagram_widget.canvas.axes.invert_yaxis()

        self.ui.actionOpenPoint.triggered.connect(lambda: self.open_file("point"))
        self.ui.actionOpenDiagram.triggered.connect(lambda: self.open_file("diagram"))
        self.ui.actionSave_Diagram.triggered.connect(lambda: self.save_diagram())
        self.ui.actionReset.triggered.connect(lambda: self.reset())
        self.ui.next_case_Button.clicked.connect(lambda: self.next_case())
        self.ui.next_step_Button.clicked.connect(lambda: self.next_step())
        self.ui.run_Button.clicked.connect(lambda: self.run_voronoi())

        # user custom case
        self.custom_case_set = set()
        self.file_case_set = None
        self.vonoroi = myVoronoiDiagram()
        self.plot_point()
        self.queue_index = 0
        self.step_cnt = 0

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
        elif self.file_case_set != None:
            # print("add point on x = {0}, y = {1}".format(x, y))
            # add point into file case
            self.file_case_set.add(tuple([x, y]))
            old_message = self.ui.messageLabel.text()
            self.ui.messageLabel.setText(old_message + "\n({0}, {1})".format(x, y))
            self.plot_point(x, y)
        else:
            print("add point on x = {0}, y = {1}".format(x, y))
            self.custom_case_set.add(tuple([x, y]))
            self.plot_point(x, y)

    def plot_point(self, x = None, y = None, point_list = None):
        self.ui.diagram_widget.canvas.axes.set_xlim([0, 600])
        self.ui.diagram_widget.canvas.axes.set_ylim([0, 600])
        self.ui.diagram_widget.canvas.axes.invert_yaxis()
        if x is not None and y is not None:
            self.ui.diagram_widget.canvas.axes.scatter(x, y, color = "blue")
        elif point_list is not None:
            for p in point_list:
                self.ui.diagram_widget.canvas.axes.scatter(p[0], p[1], color = "blue")
        self.ui.diagram_widget.canvas.draw()

    def plot_diagram(self, ele_list):
        for i in range(0, len(ele_list[1][0][0])):
            tmp_x = [ele_list[1][0][0][i], ele_list[1][1][0][i]]
            tmp_y = [ele_list[1][0][1][i], ele_list[1][1][1][i]]
            self.ui.diagram_widget.canvas.axes.plot(tmp_x, tmp_y, color = "blue")
        self.ui.diagram_widget.canvas.draw()

    def plot_convex_hull(self, ele_list):
        for i in range(0, len(ele_list[1][0][0])):
            tmp_x = [ele_list[1][0][0][i], ele_list[1][1][0][i]]
            tmp_y = [ele_list[1][0][1][i], ele_list[1][1][1][i]]
            # if self.step_cnt == 0:
            #     self.ui.diagram_widget.canvas.axes.scatter(tmp_x, tmp_y, color = "yellow")
            # elif self.step_cnt == 1:
            #     self.ui.diagram_widget.canvas.axes.scatter(tmp_x, tmp_y, color = "black")
            self.ui.diagram_widget.canvas.axes.plot(tmp_x, tmp_y, color = "red", linestyle = ':')
        self.ui.diagram_widget.canvas.draw()

    def plot_voronoi_edge(self, ele_list, color = None):
        for i in range(0, len(ele_list[1][0][0])):
            tmp_x = [ele_list[1][0][0][i], ele_list[1][1][0][i]]
            tmp_y = [ele_list[1][0][1][i], ele_list[1][1][1][i]]
            if self.step_cnt == 0:
                self.ui.diagram_widget.canvas.axes.plot(tmp_x, tmp_y, color = "blue")
            elif self.step_cnt == 1:
                self.ui.diagram_widget.canvas.axes.plot(tmp_x, tmp_y, color = "green")
            if color is not None:
                self.ui.diagram_widget.canvas.axes.plot(tmp_x, tmp_y, color = color)
        for i in range(0, len(ele_list[0][0])):
            tmp_x = ele_list[0][0][i]
            tmp_y = ele_list[0][1][i]
            if self.step_cnt == 0:
                self.ui.diagram_widget.canvas.axes.scatter(tmp_x, tmp_y, color = "blue")
            elif self.step_cnt == 1:
                self.ui.diagram_widget.canvas.axes.scatter(tmp_x, tmp_y, color = "green")
            if color is not None:
                self.ui.diagram_widget.canvas.axes.scatter(tmp_x, tmp_y, color = color)
                
        self.ui.diagram_widget.canvas.draw()

    def plot_hyperplane(self, ele_list):
        for i in range(0, len(ele_list[0][0])):
            tmp_x = [ele_list[0][0][i], ele_list[1][0][i]]
            tmp_y = [ele_list[0][1][i], ele_list[1][1][i]]
            self.ui.diagram_widget.canvas.axes.plot(tmp_x, tmp_y, color = "orange")
        self.ui.diagram_widget.canvas.draw()

    def open_file(self, type):
        try:
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
        except:
            print("error when opening {0}".format(type))
            return

    def save_diagram(self):
        try:
            filename, filepath = QFileDialog.getSaveFileName(self, 'Save File', './test_data')
            self.vonoroi.save_diagram(filename)
        except:
            print("error when saving diagram")
            return

    def next_case(self):
        self.ui.diagram_widget.reset()
        self.custom_case_set = set()
        self.file_case_set = None
        x_list, y_list = self.vonoroi.next_case()
        self.file_case_set = self.vonoroi.current_case
        if x_list == -1 or y_list == -1:
            self.ui.messageLabel.setText("End of test")
            return
        coor_info = ""
        for i in range(0, len(x_list)):
            coor_info += "({0}, {1})".format(x_list[i], y_list[i])
            if i%3 == 2:
                coor_info += "\n"
            else:
                coor_info += " "
        self.ui.messageLabel.setText("Test case: {0}\ntest coordinate:\n{1}".format(self.vonoroi.current_case_index, coor_info))
        self.ui.diagram_widget.canvas.axes.clear()
        self.plot_point(x = x_list, y = y_list)

        return
    
    def next_step(self):
        if self.queue_index < len(self.vonoroi.paint_queue):
            self.ui.diagram_widget.canvas.axes.clear()
            if self.step_cnt == 2:
                self.ui.diagram_widget.canvas.axes.set_xlim([0, 600])
                self.ui.diagram_widget.canvas.axes.set_ylim([0, 600])
                self.ui.diagram_widget.canvas.axes.invert_yaxis()
                self.plot_convex_hull(self.vonoroi.paint_queue[self.queue_index][0])
                self.plot_voronoi_edge(self.vonoroi.paint_queue[self.queue_index - 1][1], color = "green")
                self.plot_voronoi_edge(self.vonoroi.paint_queue[self.queue_index - 2][1], color = "blue")
                self.plot_hyperplane(self.vonoroi.paint_queue[self.queue_index][2])
                self.step_cnt += 1
                self.step_cnt = self.step_cnt % 3
                self.queue_index += 1
                return
            self.plot_point(point_list = self.current_case)
            self.plot_convex_hull(self.vonoroi.paint_queue[self.queue_index][0])
            self.plot_voronoi_edge(self.vonoroi.paint_queue[self.queue_index][1])
            self.step_cnt += 1
            self.step_cnt = self.step_cnt % 3
            # if self.vonoroi.paint_queue[self.queue_index][2] is not None:
            #     self.plot_hyperplane(self.vonoroi.paint_queue[self.queue_index][2])
            self.queue_index += 1
        return

    def run_voronoi(self):
        # handle the custom_case_set
        self.current_case = list()
        self.current_case.append([])
        self.current_case.append([])
        # try:
        if len(self.custom_case_set) != 0:
            for cor in self.custom_case_set:
                self.current_case[0].append(cor[0])
                self.current_case[1].append(cor[1])
        elif len(self.file_case_set) != 0:
            for cor in self.file_case_set:
                self.current_case[0].append(cor[0])
                self.current_case[1].append(cor[1])
        else:
            self.current_case = self.vonoroi.current_case
        # sorted by x value before drawing the diagram
        self.current_case = sorted(zip(*self.current_case), key = lambda x: x[0])
        draw_result = self.vonoroi.draw_voronoi_diagram(self.current_case)
        if draw_result is None and self.vonoroi.paint_queue_flag == False:
            print("cannot draw the diagram")
        elif self.vonoroi.paint_queue_flag == True:
            print("divide and conquer done, please press the next step button for display the result")
        else:
            self.plot_diagram(draw_result)
        # except:
        #     print("error when running diagram")
        #     return
        # reset custom_case_set and file_case
        self.custom_case_set = set()
        self.file_case_set = None

        return

    def reset(self):
        self.ui.diagram_widget.reset()
        self.custom_case_set = set()
        self.file_case_set = None
        self.vonoroi = myVoronoiDiagram()
        self.ui.messageLabel.setText("")
        self.vonoroi.paint_queue_flag = False
        self.vonoroi.paint_queue = list()
        self.queue_index = 0

        return