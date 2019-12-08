class DirectedSegment(object):
    """docstring for DirectedSegment"""
    def __init__(self, coordinates: list=None, point: list=None, instruction: str=None):
        super(DirectedSegment, self).__init__()
        if coordinates:
            self.x_a = coordinates[0]
            self.y_a = coordinates[1]
            self.x_b = coordinates[2]
            self.y_b = coordinates[3]
        elif point and instruction:
            # Takes initial point and follow instruction to create segment
            self.x_a = point[0]
            self.y_a = point[1]
            self.x_b = self.x_a
            self.y_b = self.y_a

            direction = instruction[0]

            if direction=='R':
                self.x_b = self.x_a + int(instruction[1:])
            elif direction=='U':
                self.y_b = self.y_a + int(instruction[1:])
            elif direction=='L':
                self.x_b = self.x_a - int(instruction[1:])
            elif direction=='D':
                self.y_b = self.y_a - int(instruction[1:])


        self.left = min(self.x_a, self.x_b)
        self.right = max(self.x_a, self.x_b)
        self.top = max(self.y_a, self.y_b)
        self.bottom = min(self.y_a, self.y_b)

        self.vertical = (self.x_a == self.x_b)



    def cross(self, segment):
        if self.vertical == segment.vertical:
            if self.vertical and self.x_a == segment.x_a:
                if self.bottom < segment.bottom:
                    bottom_seg = self
                    top_seg = segment
                else:
                    bottom_seg = segment
                    top_seg = self
                if bottom_seg.top >= top_seg.bottom:
                    return [[self.x_a, i] for i in range(top_seg.bottom, min(bottom_seg.top, top_seg.top)+1)]
            elif (not self.vertical) and self.y_a == segment.y_a:
                if self.left < segment.left:
                    left_seg = self
                    right_seg = segment
                else:
                    left_seg = segment
                    right_seg = self
                if left_seg.right >= right_seg.left:
                    return [[i, self.y_a] for i in range(right_seg.left, min(left_seg.right, right_seg.right)+1)]

        else:
            if self.vertical:
                vertical = self
                horizontal = segment
            else:
                vertical = segment
                horizontal = self

            if vertical.bottom <= horizontal.bottom:
                if vertical.top >= horizontal.top:
                    if horizontal.left <= vertical.left:
                        if horizontal.right >= vertical.right:
                            return [vertical.left, horizontal.top]

        return False


def create_segment_list(instructions: list):
    point = [0, 0]
    seg_list = []

    for tmp_inst in instructions:
        segment = DirectedSegment(point=point, instruction=tmp_inst)
        point = [segment.x_b, segment.y_b]
        seg_list.append(segment)

    return seg_list


def distance_manhattan(point):
    return abs(point[0]) + abs(point[1])


def step_intersection(instructions, point):
    current_point = [0, 0]
    steps_count = 0

    if point == [0, 0]:
        return 0 

    for tmp_inst in instructions:
        direction = tmp_inst[0]
        step = int(tmp_inst[1:])

        if direction=='R':
            if (point[1] == current_point[1]) and (current_point[0] < point[0]) and (current_point[0] + step >= point[0]):
                steps_count += abs(point[0] - current_point[0])
                break
            else:
                steps_count += step
                current_point[0] += step

        if direction=='L':
            if (point[1] == current_point[1]) and (current_point[0] > point[0]) and (current_point[0] - step <= point[0]):
                steps_count += abs(point[0] - current_point[0])
                break
            else:
                steps_count += step
                current_point[0] -= step

        if direction=='U':
            if (point[0] == current_point[0]) and (current_point[1] < point[1]) and (current_point[1] + step >= point[1]):
                steps_count += abs(point[1] - current_point[1])
                break
            else:
                steps_count += step
                current_point[1] += step

        if direction=='D':
            if (point[0] == current_point[0]) and (current_point[1] > point[1]) and (current_point[1] - step <= point[1]):
                steps_count += abs(point[1] - current_point[1]) 
                break
            else:
                steps_count += step
                current_point[1] -= step

    return steps_count


if __name__=='__main__':
    with open("input.csv", mode='r') as input_file:
        instructions = input_file.read().split("\n")
        line_1 = instructions[0].split(',')
        line_2 = instructions[1].split(',')

        seg_list_1 = create_segment_list(line_1)
        seg_list_2 = create_segment_list(line_2)

        list_crossing = []
        for seg_1 in seg_list_1:
            for seg_2 in seg_list_2:
                crossing = seg_1.cross(seg_2)
                if crossing:
                    if type(crossing[0]) == list:
                        list_crossing += crossing
                    else:
                        list_crossing.append(crossing)

        list_dist = [distance_manhattan(x) for x in list_crossing if distance_manhattan(x) != 0]

        print("Answer #3.1: ", min(list_dist))

        s1 = DirectedSegment(coordinates=[0, 0, 0, 10])
        s2 = DirectedSegment(coordinates=[0, 1, 0, 7])

        print(s1.cross(s2))



        # Remove (0,0) intersection
        list_crossing = list_crossing[1:]

        list_steps = []
        for tmp_crossing in list_crossing:
            list_steps.append(step_intersection(line_1, tmp_crossing) + step_intersection(line_2, tmp_crossing))

        print(list_steps)

        print("Answer #3.2: ", min(list_steps))
