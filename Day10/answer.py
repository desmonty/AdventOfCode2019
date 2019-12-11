from fractions import gcd
import numpy as np

PI = 3.1415926535


def unit_vector(vec):
    return vec / np.linalg.norm(vec)


def angle(v1, v2):
    if v2[0] - v1[0] == 0:
        return PI if v2[1] > v1[1] else 0

    v2 = unit_vector((v2[0] - v1[0], - v2[1] + v1[1]))
    v1 = (0, 1)

    angle_value = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))

    if v2[0] < 0:
        angle_value = 2 * PI - angle_value

    return angle_value


def compute_seen_asteroid(asteroid_map: list, position: list):
    """
    asteroid_map: list of list giving the asteroid placement.
    position: [X, Y]
    """
    seen = 0
    for pos_y, line in enumerate(asteroid_map):
        for pos_x, asteroid_tmp in enumerate(line):
            is_ast = asteroid_tmp == '#'
            if is_ast and (pos_x != position[0] or pos_y != position[1]):
                x_diff = pos_x - position[0]
                y_diff = pos_y - position[1]
                gcd_asteroid = abs(gcd(x_diff, y_diff))
                visible = True
                for increment in range(1, gcd_asteroid):
                    inter_x = position[0] + increment * int(x_diff / gcd_asteroid)
                    inter_y = position[1] + increment * int(y_diff / gcd_asteroid)
                    tmp_ast = asteroid_map[inter_y][inter_x]
                    if tmp_ast == '#':
                        visible = False
                        break
                if visible:
                    seen += 1
    return seen


def best_station(asteroid_map: list):
    """
    return best_position and number of asteroid seen
    """
    best_position = []
    best_num_asteroid = -1
    for pos_y, line in enumerate(asteroid_map):
        for pos_x, asteroid_tmp in enumerate(line):
            if asteroid_tmp == '#':
                asteroid_seen = compute_seen_asteroid(asteroid_map, [pos_x, pos_y])
                if asteroid_seen > best_num_asteroid:
                    best_position = [pos_x, pos_y]
                    best_num_asteroid = asteroid_seen

    return(best_position, best_num_asteroid)


def list_asteroid(asteroid_map: list, position: list) -> list:
    """
    """
    list_asteroid = []
    for pos_y, line in enumerate(asteroid_map):
        for pos_x, asteroid_tmp in enumerate(line):
            same_ast = (pos_x == position[0]) and (pos_y == position[1])
            if asteroid_tmp == '#' and not same_ast:
                x_diff = pos_x - position[0]
                y_diff = pos_y - position[1]
                gcd_asteroid = abs(gcd(x_diff, y_diff))
                prio = 0
                for increment in range(1, gcd_asteroid):
                    inter_x = position[0] + increment * int(x_diff / gcd_asteroid)
                    inter_y = position[1] + increment * int(y_diff / gcd_asteroid)
                    if asteroid_map[inter_y][inter_x] == '#':
                        prio += 1
                list_asteroid.append((prio, angle(position, [pos_x, pos_y]), pos_x, pos_y))
    return sorted(list_asteroid)

if __name__ == '__main__':
    asteroid_map = []
    with open('input.csv', mode='r') as asteroid_input:
        asteroid_map = asteroid_input.read().split('\n')

    best_position, best_num_asteroid = best_station(asteroid_map)

    print("Answer #10.1: ", best_position, best_num_asteroid)

    _, _, x_200, y_200 = list_asteroid(asteroid_map, best_position)[199]
    print("Answer #10.2: ", x_200, y_200)