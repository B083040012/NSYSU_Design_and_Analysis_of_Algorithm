import numpy as np

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
                    x_list = list()
                    y_list = list()
                    for num in range(0, dot_num):
                        input = in_file.readline()
                        input = input.strip()
                        x, y = input.split(' ')
                        x, y = int(x), int(y)
                        x_list.append(x)
                        y_list.append(y)
                    self.test_case_list.append([x_list, y_list])
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
            # print(self.diagram_ele_list)
        else: return -1
        # for sublist in self.test_case_list:
        #     print(sublist)
        return 0

    def next_case(self):
        self.current_case_index += 1
        if self.current_case_index >= len(self.test_case_list):
            print("end of test case")
            return -1, -1
        self.current_case = self.test_case_list[self.current_case_index]
        return self.current_case[0], self.current_case[1]