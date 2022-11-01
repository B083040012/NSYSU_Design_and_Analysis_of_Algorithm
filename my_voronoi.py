from os import remove
from pickle import FALSE
import numpy as np
import math

class myVoronoiDiagram():
    def __init__(self):
        self.test_case_list = list()
        """
        2 (point or edge)
        point: x_list, y_list
        edge: start_list(x_list, y_list), end_list(x_list, y_list)
        """
        self.diagram_ele_list = None
        self.current_case_index = -1
        self.current_case = None

    def read_file(self, filename, type):
        try:
            in_file = open(filename, mode = 'r', errors = 'ignore')
        except:
            return -1
        
        if type == "point":
            while True:
                line = in_file.readline()
                if not line:
                    break
                line = line.strip()
                # print(line)
                if line == "":
                    continue
                elif line[0] == '#':
                    continue
                elif line[0] == '0':
                    print("end of test data")
                    return 0
                else:
                    dot_num = int(line)
                    dot_set = set()
                    for num in range(0, dot_num):
                        input = in_file.readline()
                        input = input.strip()
                        x, y = input.split(' ')
                        x, y = int(x), int(y)
                        dot_set.add(tuple([x, y]))
                    self.test_case_list.append(dot_set)
        elif type == "diagram":
            self.diagram_ele_list = [[[] for k in range(2)] for i in range(2)]
            for i in range(2): 
                self.diagram_ele_list[1][0].append([])
                self.diagram_ele_list[1][1].append([])
            while True:
                line = in_file.readline()
                if not line:
                    break
                line = line.strip()
                if line == '':
                    continue
                elif line[0] == 'P':
                    trash, x, y = line.split(' ')
                    x, y = int(x), int(y)
                    self.diagram_ele_list[0][0].append(x)
                    self.diagram_ele_list[0][1].append(y)
                elif line[0] == 'E':
                    trash, x1, y1, x2, y2 = line.split()
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    self.diagram_ele_list[1][0][0].append(x1)
                    self.diagram_ele_list[1][0][1].append(y1)
                    self.diagram_ele_list[1][1][0].append(x2)
                    self.diagram_ele_list[1][1][1].append(y2)
        else: return -1
        return 0

    def save_diagram(self, filename):

        """
        Save the lastest drawn diagram
            * according to the style by HW instruction
            * first sort the point list and edge list
        """
        point_list = list()
        edge_list = list()
        save_file = open(filename,'w')
        for point_index in range(len(self.last_diagram[0][0])):
            point_list.append((self.last_diagram[0][0][point_index], self.last_diagram[0][1][point_index]))
        point_list = sorted(point_list)
        for point in point_list:
            save_file.write("P ")
            save_file.write("{0} {1}\n".format(point[0], point[1]))
        for edge_index in range(len(self.last_diagram[1][0][0])):
            tmp_list = [(self.last_diagram[1][0][0][edge_index], self.last_diagram[1][0][1][edge_index]), \
                (self.last_diagram[1][1][0][edge_index], self.last_diagram[1][1][1][edge_index])]
            tmp_list = sorted(tmp_list)
            tmp_edge = (tmp_list[0][0], tmp_list[0][1], tmp_list[1][0], tmp_list[1][1])
            edge_list.append(tmp_edge)
        edge_list = sorted(edge_list)
        for edge in edge_list:
            save_file.write("E ")
            save_file.write("{0} {1} {2} {3}\n".format(edge[0], edge[1], edge[2], edge[3]))
        save_file.close()

    def next_case(self):
        self.current_case_index += 1
        if self.current_case_index >= len(self.test_case_list):
            print("end of test case")
            return -1, -1
        self.current_case = self.test_case_list[self.current_case_index]
        tmp_point_list = list()
        tmp_point_list.append([])
        tmp_point_list.append([])
        if len(self.current_case) != 0:
            for cor in self.current_case:
                tmp_point_list[0].append(cor[0])
                tmp_point_list[1].append(cor[1])
        return tmp_point_list[0], tmp_point_list[1]

    def get_circumcenter(self, point_set):
        x1, y1 = point_set[0][0], point_set[0][1]
        x2, y2 = point_set[1][0], point_set[1][1]
        x3, y3 = point_set[2][0], point_set[2][1]
        d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        try:
            ux = ((x1 * x1 + y1 * y1) * (y2 - y3) + (x2 * x2 + y2 * y2) * (y3 - y1) + (x3 * x3 + y3 * y3) * (y1 - y2)) / d
            uy = ((x1 * x1 + y1 * y1) * (x3 - x2) + (x2 * x2 + y2 * y2) * (x1 - x3) + (x3 * x3 + y3 * y3) * (x2 - x1)) / d
            return int(ux), int(uy)
        except:
            return -1, -1

    def valid_p_list(self, p, edge_vector = None, circumcenter = None):
        if p[0] < 0 or p[0] > 600 or p[1] < 0 or p[1] > 600:
            return False
        elif (circumcenter is not None) and (edge_vector is not None) and \
            (((p[0] - circumcenter[0]) * edge_vector[0] < 0) or ((p[1] - circumcenter[1]) * edge_vector[1] < 0)):
            return False
        return True

    def draw_voronoi_diagram(self, point_set):
        point_num = len(point_set)
        if point_num == 1:
            print("1 point case, ignore")
            self.last_diagram = None
            return None
        draw_diagram_ele_list = [[[] for k in range(2)] for i in range(2)]
        for i in range(2): 
            draw_diagram_ele_list[1][0].append([])
            draw_diagram_ele_list[1][1].append([])
        # add point into ele list
        for i in range(0, len(point_set)):
            draw_diagram_ele_list[0][0].append(point_set[i][0])
            draw_diagram_ele_list[0][1].append(point_set[i][1])
        if point_num == 2:
            print("2-point case")
            midpoint = [int((point_set[0][0] + point_set[1][0]) / 2), int((point_set[0][1] + point_set[1][1]) / 2)]
            if (point_set[1][1] - point_set[0][1]) == 0:
                # two points are horizontal
                p_list = [[midpoint[0], 0], [midpoint[0], 600]]
            elif (point_set[1][0] - point_set[0][0]) == 0:
                # two points are vertical
                p_list = [[0, midpoint[1]], [600, midpoint[1]]]
            else:
                slope = -(point_set[1][0] - point_set[0][0]) / (point_set[1][1] - point_set[0][1])
                tmp_list = [[0, midpoint[1] - slope * midpoint[0]], [600, midpoint[1] + (600 - midpoint[0]) * slope], \
                    [midpoint[0] - (midpoint[1] / slope), 0], [midpoint[0] + (600 - midpoint[1]) / slope, 600]]
                p_list = [p for p in tmp_list if self.valid_p_list(p)]
            # ensure that start and end point are on the canvas edge
            start_p, end_p = p_list[0], p_list[1]
            draw_diagram_ele_list[1][0][0].append(int(start_p[0]))
            draw_diagram_ele_list[1][0][1].append(int(start_p[1]))
            draw_diagram_ele_list[1][1][0].append(int(end_p[0]))
            draw_diagram_ele_list[1][1][1].append(int(end_p[1]))

        elif point_num == 3:
            print("3-point case")
            circumcenter_x, circumcenter_y = self.get_circumcenter(point_set)
            """
            Three point on same line: execute 2-point case twice
            """
            if circumcenter_x == -1:
                print("on the same line")
                if point_set[0][0] == point_set[1][0]:
                    # same x value: sorted by y value
                    point_set = sorted(point_set, key = lambda x: x[1])
                point_set_part_list = list()
                point_set_part_list.append(point_set[0:2]); point_set_part_list.append(point_set[1:3])
                for point_set_part in point_set_part_list:
                    tmp_ele_list = self.draw_voronoi_diagram(point_set_part)
                    draw_diagram_ele_list[1][0][0].append(int(tmp_ele_list[1][0][0][0]))
                    draw_diagram_ele_list[1][0][1].append(int(tmp_ele_list[1][0][1][0]))
                    draw_diagram_ele_list[1][1][0].append(int(tmp_ele_list[1][1][0][0]))
                    draw_diagram_ele_list[1][1][1].append(int(tmp_ele_list[1][1][1][0]))
                self.last_diagram = draw_diagram_ele_list
                return draw_diagram_ele_list
            circumcenter = [circumcenter_x, circumcenter_y]
            """
            For each bisector:
                1. check the angle of two vector
                2. if angle <= 90:
                        vector = {circumcenter --> midpoint}
                   else:
                        vector = - {circumcenter -->  midpoint}
                3. find the start point and end point by vector
            """
            for i in range(3):
                p1_index = (i + 1) % 3; p2_index = (i + 2) % 3
                vector_p1 = [point_set[p1_index][0] - point_set[i][0], point_set[p1_index][1] - point_set[i][1]]
                vector_p2 = [point_set[p2_index][0] - point_set[i][0], point_set[p2_index][1] - point_set[i][1]]
                midpoint = [int((point_set[p1_index][0]+ point_set[p2_index][0]) / 2), int((point_set[p1_index][1] + point_set[p2_index][1]) / 2)]
                """
                Default edge_vector: circumcenter--> intersection
                """
                edge_vector = [midpoint[0] - circumcenter[0], midpoint[1] - circumcenter[1]]
                """
                For triangle that edge_vector = [0, 0] (midpoint = circumcenter)
                Recalculate the edge_vector
                """
                if edge_vector[0] == 0 and edge_vector[1] == 0:
                    print("90 degree, circumcenter = midpoint")
                    edge_vector = [vector_p1[0] + vector_p2[0], vector_p1[1] + vector_p2[1]]
                elif np.dot(vector_p1, vector_p2) < 0:
                    print("greater and equal than 90 degree")
                    edge_vector[0] = -edge_vector[0]
                    edge_vector[1] = -edge_vector[1]
                if edge_vector[0] == 0:
                    p_list = [[midpoint[0], 0], [midpoint[0], 600]]
                elif edge_vector[1] == 0:
                    p_list = [[0, midpoint[1]], [600, midpoint[1]]]
                else:
                    slope = edge_vector[1] / edge_vector[0]
                    tmp_list = [[0, midpoint[1] - slope * midpoint[0]], [600, midpoint[1] + (600 - midpoint[0]) * slope], \
                        [midpoint[0] - (midpoint[1] / slope), 0], [midpoint[0] + (600 - midpoint[1]) / slope, 600]]
                    # remove points outside the canvas and points not on the same direction as edge_vector
                    p_list = [p for p in tmp_list if self.valid_p_list(p, edge_vector, circumcenter)]
                """
                Ensure that the edge will be shown in the GUI window
                """
                end_p = p_list[0]
                if circumcenter[0] < 0 or circumcenter[0] > 600 or circumcenter[0] < 0 or circumcenter[1] > 600:
                    # circumcenter is outside the canvas, adject the start_p
                    start_p = p_list[1]
                else:
                    start_p = circumcenter
                draw_diagram_ele_list[1][0][0].append(int(start_p[0]))
                draw_diagram_ele_list[1][0][1].append(int(start_p[1]))
                draw_diagram_ele_list[1][1][0].append(int(end_p[0]))
                draw_diagram_ele_list[1][1][1].append(int(end_p[1]))
                
        else:
            print("4-point or more: currently cannot deal with")
            draw_diagram_ele_list = None

        self.last_diagram = draw_diagram_ele_list
        return draw_diagram_ele_list