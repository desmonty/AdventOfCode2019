from fractions import gcd

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

if __name__ == '__main__':
    asteroid_map = []
    with open('input.csv', mode='r') as asteroid_input:
        asteroid_map = asteroid_input.read().split('\n')

    best_position = []
    best_num_asteroid = -1
    for pos_y, line in enumerate(asteroid_map):
        for pos_x, asteroid_tmp in enumerate(line):
            if asteroid_tmp == '#':
                asteroid_seen = compute_seen_asteroid(asteroid_map, [pos_x, pos_y])
                if asteroid_seen > best_num_asteroid:
                    best_position = [pos_x, pos_y]
                    best_num_asteroid = asteroid_seen

    print("Answer #10.1: ", best_position, best_num_asteroid)