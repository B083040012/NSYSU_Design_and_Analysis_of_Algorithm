from heapq import merge
from xmlrpc.client import MAXINT
import numpy as np

class voronoiEdge():
    def __init__(self):
        self.p1 = None
        self.p2 = None
        self.start_point = None
        self.end_point = None

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
        self.paint_queue = list()

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
                    tmp_list = [[midpoint[0], 0], [midpoint[0], 600]]
                    p_list = [p for p in tmp_list if ((p[1] - circumcenter[1]) * edge_vector[1] >= 0)]
                elif edge_vector[1] == 0:
                    tmp_list = [[0, midpoint[1]], [600, midpoint[1]]]
                    p_list = [p for p in tmp_list if ((p[0] - circumcenter[0]) * edge_vector[0] >= 0)]
                else:
                    slope = edge_vector[1] / edge_vector[0]
                    tmp_list = [[0, midpoint[1] - slope * midpoint[0]], [600, midpoint[1] + (600 - midpoint[0]) * slope], \
                        [midpoint[0] - (midpoint[1] / slope), 0], [midpoint[0] + (600 - midpoint[1]) / slope, 600]]
                    # remove points outside the canvas and points not on the same direction as edge_vector
                    p_list = [p for p in tmp_list if self.valid_p_list(p, edge_vector, circumcenter)]
                """
                Ensure that the edge will be shown in the GUI window
                """
                if len(p_list) > 0:
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
                
        elif point_num >= 4:
            self.divide_and_conquer(point_set)
            self.paint_queue_flag = True
            print("len of paint_queue: {0}".format(len(self.paint_queue)))
            return None

        self.last_diagram = draw_diagram_ele_list
        return draw_diagram_ele_list

    def draw_voronoi_divide_and_conquer(self, point_set):
        point_num = len(point_set)
        if point_num == 1:
            print("1 point case, ignore")
            self.last_diagram = None
            return None
        voronoi_edge_list = list()
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
            voronoi_edge_tmp = voronoiEdge()
            voronoi_edge_tmp.start_point = tuple([int(start_p[0]), int(start_p[1])])
            voronoi_edge_tmp.end_point = tuple([int(end_p[0]), int(end_p[1])])
            voronoi_edge_tmp.p1 = point_set[0]
            voronoi_edge_tmp.p2 = point_set[1]
            voronoi_edge_list.append(voronoi_edge_tmp)
            return voronoi_edge_list

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
                    voronoi_edge_tmp = voronoiEdge()
                    voronoi_edge_tmp.p1 = tuple(point_set_part[0])
                    voronoi_edge_tmp.p2 = tuple(point_set_part[1])
                    tmp_ele_list = self.draw_voronoi_diagram(point_set_part)
                    voronoi_edge_tmp.start_point = tuple([int(tmp_ele_list[1][0][0][0]), int(tmp_ele_list[1][0][1][0])])
                    voronoi_edge_tmp.end_point = tuple([int(tmp_ele_list[1][1][0][0]), int(tmp_ele_list[1][1][1][0])])
                    voronoi_edge_list.append(voronoi_edge_tmp)
                    # draw_diagram_ele_list[1][0][0].append(int(tmp_ele_list[1][0][0][0]))
                    # draw_diagram_ele_list[1][0][1].append(int(tmp_ele_list[1][0][1][0]))
                    # draw_diagram_ele_list[1][1][0].append(int(tmp_ele_list[1][1][0][0]))
                    # draw_diagram_ele_list[1][1][1].append(int(tmp_ele_list[1][1][1][0]))
                # self.last_diagram = draw_diagram_ele_list
                return voronoi_edge_list
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
                    tmp_list = [[midpoint[0], 0], [midpoint[0], 600]]
                    p_list = [p for p in tmp_list if ((p[1] - circumcenter[1]) * edge_vector[1] >= 0)]
                elif edge_vector[1] == 0:
                    tmp_list = [[0, midpoint[1]], [600, midpoint[1]]]
                    p_list = [p for p in tmp_list if ((p[0] - circumcenter[0]) * edge_vector[0] >= 0)]
                else:
                    slope = edge_vector[1] / edge_vector[0]
                    tmp_list = [[0, midpoint[1] - slope * midpoint[0]], [600, midpoint[1] + (600 - midpoint[0]) * slope], \
                        [midpoint[0] - (midpoint[1] / slope), 0], [midpoint[0] + (600 - midpoint[1]) / slope, 600]]
                    # remove points outside the canvas and points not on the same direction as edge_vector
                    p_list = [p for p in tmp_list if self.valid_p_list(p, edge_vector, circumcenter)]
                """
                Ensure that the edge will be shown in the GUI window
                """
                if len(p_list) > 0:
                    end_p = p_list[0]
                    if circumcenter[0] < 0 or circumcenter[0] > 600 or circumcenter[0] < 0 or circumcenter[1] > 600:
                        # circumcenter is outside the canvas, adject the start_p
                        start_p = p_list[1]
                    else:
                        start_p = circumcenter
                    voronoi_edge_tmp = voronoiEdge()
                    voronoi_edge_tmp.start_point = tuple([int(start_p[0]), int(start_p[1])])
                    voronoi_edge_tmp.end_point = tuple([int(end_p[0]), int(end_p[1])])
                    voronoi_edge_tmp.p1 = tuple(point_set[p1_index])
                    voronoi_edge_tmp.p2 = tuple(point_set[p2_index])
                    voronoi_edge_list.append(voronoi_edge_tmp)
            return voronoi_edge_list

    def divide_and_conquer(self, point_set):
        """
        split the point set with n/2 points
        """
        if len(point_set) > 3:
            sl = point_set[0:int(len(point_set) / 2)]
            sr = point_set[int(len(point_set) / 2):]
            print("sl: {0}, sr: {1}".format(sl, sr))

            convex_hull_left, voronoi_edge_list_left = self.divide_and_conquer(sl)
            convex_hull_right, voronoi_edge_list_right = self.divide_and_conquer(sr)
            self.add_to_paint_queue(convex_hull_left, voronoi_edge_list_left)
            self.add_to_paint_queue(convex_hull_right, voronoi_edge_list_right)

        else:
            voronoi_edge_list = self.draw_voronoi_divide_and_conquer(point_set)
            return point_set, voronoi_edge_list

        print("convex_hull_left: {0}".format(convex_hull_left))
        print("convex_hull_right: {0}".format(convex_hull_right))

        u, r = self.lower_common_support(convex_hull_left, convex_hull_right)
        lsp_line = [u, r]
        check_line = [u, r]
        u, r = self.upper_common_support(convex_hull_left, convex_hull_right)
        usp_line = [u, r]
        hyperplane_list = list()
        """
        w0: point at infinity downward
        """
        midpoint = [int((lsp_line[0][0] + lsp_line[1][0]) / 2), int((lsp_line[0][1] + lsp_line[1][1]) / 2)]
        slope = -(lsp_line[0][0] - lsp_line[1][0]) / (lsp_line[0][1] - lsp_line[1][1])
        # tmp_list = [[0, midpoint[1] - slope * midpoint[0]], [600, midpoint[1] + (600 - midpoint[0]) * slope], \
        #                 [midpoint[0] - (midpoint[1] / slope), 0], [midpoint[0] + (600 - midpoint[1]) / slope, 600]]
        if int(midpoint[0] - (midpoint[1] / slope)) >= 0:
            w0 = [int(midpoint[0] - (midpoint[1] / slope)), 0]
            current_line = [w0, midpoint]
        elif int(midpoint[1] - slope * midpoint[0]) >= 0 and int(midpoint[1] - slope * midpoint[0]) < int(midpoint[1] + (600 - midpoint[0]) * slope):
            w0 = [0, int( midpoint[1] - slope * midpoint[0])]
            current_line = [w0, midpoint]
        elif int(midpoint[1] + (600 - midpoint[0]) * slope) >= 0 and int(midpoint[1] + (600 - midpoint[0]) * slope) < int(midpoint[1] - slope * midpoint[0]):
            w0 = [midpoint[0] + (600 - midpoint[1]) / slope, 600]
            current_line = [w0, midpoint]
        # tmp_list = [[0, midpoint[1] - slope * midpoint[0]], [midpoint[0] - (midpoint[1] / slope), 0]]
        intersection = w0
        print("w0: {0}, intersection: {1}".format(w0, intersection))
        cnt = 0
        while check_line[0] != usp_line[0] or check_line[1] != usp_line[1]:
            cnt += 1
            if cnt >= 5: break
            left_intersection = [MAXINT, MAXINT]
            right_intersection = [MAXINT, MAXINT]
            left_new_point = check_line[0]
            for edge in (voronoi_edge_list_left):
                if (check_line[0] == edge.p1 or check_line[0] == edge.p2):
                    x, y = self.intersection(current_line[0], current_line[1], edge.start_point, edge.end_point)
                    if y <= intersection[1] + 1: continue
                    if y < left_intersection[1]: 
                        left_intersection = [x, y]
                        if check_line[0] == edge.p1:
                            left_new_point = edge.p2
                        elif check_line[0] == edge.p2:
                            left_new_point = edge.p1
                        # current_line = [intersection, [(check_line[0][0] + check_line[0][1]) / 2, (check_line[1][0] + check_line[1][1]) / 2]]
                        # hyperplane_list.append([w0, intersection])
                        # w0 = intersection
            right_new_point = check_line[1]
            for edge in (voronoi_edge_list_right):
                if (check_line[1] == edge.p1 or check_line[1] == edge.p2):
                    x, y = self.intersection(current_line[0], current_line[1], edge.start_point, edge.end_point)
                    if y <= intersection[1] + 1: continue
                    if y < right_intersection[1]: 
                        right_intersection = [x, y]
                        if check_line[1] == edge.p1:
                            right_new_point = edge.p2
                        elif check_line[1] == edge.p2:
                            right_new_point = edge.p1
                        # current_line = [intersection, [(check_line[0][0] + check_line[0][1]) / 2, (check_line[1][0] + check_line[1][1]) / 2]]
                        # hyperplane_list.append([w0, intersection])
                        # w0 = intersection
            if left_intersection[1] < right_intersection[1]:
                intersection = left_intersection
                check_line[0] = left_new_point
            else:
                intersection = right_intersection
                check_line[1] = right_new_point
            current_line = [intersection, [(check_line[0][0] + check_line[1][0]) / 2, (check_line[0][1] + check_line[1][1]) / 2]]
            print("check_line: {0}, {1}".format(check_line[0], check_line[1]))
            print("w0: {0}, intersection: {1}".format(w0, intersection))
            hyperplane_list.append([w0, intersection])
            # print("w0: {0}, intersection: {1}".format(w0, intersection))
            w0 = intersection
        slope = -(check_line[0][0] - check_line[1][0]) / (check_line[0][1] - check_line[1][1])
        if intersection[0] + (600 - intersection[1]) / slope >= 0 and 600 > intersection[1]:
            hyperplane_list.append([intersection, [intersection[0] + (600 - intersection[1]) / slope, 600]])
        elif intersection[1] + (600 - intersection[0]) * slope > intersection[1]:
            hyperplane_list.append([intersection, [600, intersection[1] + (600 - intersection[0]) * slope]])
        elif intersection[1] - slope * intersection[0] > intersection[1]:
            hyperplane_list.append([intersection, [0, intersection[1] - slope * intersection[0]]])

        merge_convex_hull_point_set = self.merge_convex_hull(convex_hull_left + convex_hull_right)
        merge_voronoi_edge_list = voronoi_edge_list_left + voronoi_edge_list_right
        print("merge_convex_hull_point_set: {0}".format(merge_convex_hull_point_set))
        print("merge_voronoi_edge_list: {0}".format(merge_voronoi_edge_list))
        print("hyperplane: {0}".format(hyperplane_list))
        self.add_to_paint_queue(merge_convex_hull_point_set, merge_voronoi_edge_list, hyperplane_list)

        return merge_convex_hull_point_set, merge_voronoi_edge_list

    def intersection(self, a, b, c, d):
        a1 = b[1] - a[1]
        b1 = a[0] - b[0]
        c1 = a1 * a[0] + b1 * a[1]

        a2 = d[1] - c[1]
        b2 = c[0] - d[0]
        c2 = a2 * c[0] + b2 * c[1]

        determinanat = a1 * b2 - a2 * b1

        if determinanat == 0:
            print("parallel!")
        else:
            x = int((b2 * c1 - b1 * c2) / determinanat)
            y = int((a1 * c2 - a2 * c1) / determinanat)
            return x, y

    def lower_common_support(self, convex_hull_left, convex_hull_right):
        pl = sorted(convex_hull_left)
        pr = sorted(convex_hull_right)
        u,r = pl[-1], pr[0]
        for p in pl:
            d = (p[0] - u[0]) * (r[1] - u[1]) - (p[1] - u[1]) * (r[0] - u[0])
            if d > 0: u = p
        for p in pr:
            d = (p[0] - u[0]) * (r[1] - u[1]) - (p[1] - u[1]) * (r[0] - u[0])
            if d > 0: r = p
        print("lower_common_support: u:{0}, r:{1}".format(u, r))
        return u,r

    def upper_common_support(self, convex_hull_left, convex_hull_right):
        pl = sorted(convex_hull_left)
        pr = sorted(convex_hull_right)
        u,r = pl[-1], pr[0]
        for p in pl:
            d = (p[0] - u[0]) * (r[1] - u[1]) - (p[1] - u[1]) * (r[0] - u[0])
            if d < 0: u = p
        for p in pr:
            d = (p[0] - u[0]) * (r[1] - u[1]) - (p[1] - u[1]) * (r[0] - u[0])
            if d < 0: r = p
        print("upper_common_support: u:{0}, r:{1}".format(u, r))
        return u,r

    def add_to_paint_queue(self, point_set, edge_list, hyperplane_list = None):
        paint_tmp = [[[] for k in range(2)] for i in range(2)]
        edge_tmp = [[[] for k in range(2)] for i in range(2)]
        hyperplane_tmp = None

        for i in range(2): 
            paint_tmp[1][0].append([])
            paint_tmp[1][1].append([])
            edge_tmp[1][0].append([])
            edge_tmp[1][1].append([])
        # add point into ele list
        for i in range(0, len(point_set)):
            paint_tmp[0][0].append(point_set[i][0])
            paint_tmp[0][1].append(point_set[i][1])
        for i in range(0, len(edge_list)):
            edge_tmp[0][0].append(edge_list[i].p1[0])
            edge_tmp[0][1].append(edge_list[i].p1[1])
            edge_tmp[0][0].append(edge_list[i].p2[0])
            edge_tmp[0][1].append(edge_list[i].p2[1])
            edge_tmp[1][0][0].append(edge_list[i].start_point[0])
            edge_tmp[1][0][1].append(edge_list[i].start_point[1])
            edge_tmp[1][1][0].append(edge_list[i].end_point[0])
            edge_tmp[1][1][1].append(edge_list[i].end_point[1])
        for i in range(len(point_set)):
            paint_tmp[1][0][0].append(point_set[i][0])
            paint_tmp[1][0][1].append(point_set[i][1])
            paint_tmp[1][1][0].append(point_set[(i + 1) % len(point_set)][0])
            paint_tmp[1][1][1].append(point_set[(i + 1) % len(point_set)][1])

        if hyperplane_list is not None:
            hyperplane_tmp =[[[] for k in range(2)] for i in range(2)]
            for i in range(len(hyperplane_list)):
                hyperplane_tmp[0][0].append(hyperplane_list[i][0][0])
                hyperplane_tmp[0][1].append(hyperplane_list[i][0][1])
                hyperplane_tmp[1][0].append(hyperplane_list[i][1][0])
                hyperplane_tmp[1][1].append(hyperplane_list[i][1][1])

        self.paint_queue.append([paint_tmp, edge_tmp, hyperplane_tmp])

    def cross(self, point_o, point_a, point_b):
        return (point_a[0] - point_o[0]) * (point_b[1] - point_o[1]) - \
                (point_a[1] - point_o[1]) * (point_b[0] - point_o[0])

    def merge_convex_hull(self, merge_convex_point_set):
        result = list()
        point_set = sorted(merge_convex_point_set)
        print("merge_convex_point set: {0}".format(point_set))
        # print("merge_convex_point set: {0}".format(merge_convex_point_set))

        m = 0
        for i in range(len(point_set)):
            while(m >= 2 and self.cross(result[m - 2], result[m - 1], point_set[i]) <= 0):
                m -= 1
                del result[m]
            result.append(point_set[i])
            m += 1
        t = m + 1
        for i in range(len(point_set) - 2, -1, -1):
            while(m >= t and self.cross(result[m - 2], result[m - 1], point_set[i]) <= 0):
                m -= 1
                del result[m]
            result.append(point_set[i])
            m += 1
        m -= 1
        return result