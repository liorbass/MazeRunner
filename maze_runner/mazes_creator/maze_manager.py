import math
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np

from .maze_consts import WALL, USER_POS, OPEN, UNSEEN, END, VISITED_POS


# from daedalus import Maze
# from daedalus._maze import init_random
# from maze_consts import WALL, USER_POS, OPEN, UNSEEN, END, VISITED_POS


def _get_maze_at_pos(maze: np.array, pos: (int, int)):
    if ((pos[0] < maze.shape[0] and pos[0] >= 0) and
            (pos[1] < maze.shape[1] and pos[1] >= 0)):
        res = maze[pos[0]][pos[1]]
        return res
    else:
        return -1


def _set_maze_at_post(maze: np.array, pos: (int, int), val: int):
    if pos[1] >= len(maze) or pos[0] >= len(maze):
        return maze
    if _get_maze_at_pos(maze, pos) == VISITED_POS:
        return maze
    maze[pos[0]][pos[1]] = val
    return maze


def _revel_in_1_pos(new_maze, old_maze, pos):
    res = 0
    if _get_maze_at_pos(new_maze, pos) == UNSEEN:
        res = 1
    val = _get_maze_at_pos(old_maze, pos)
    _set_maze_at_post(new_maze, pos, val)
    return res


def _revel_in_pos(new_maze, old_maze, pos):
    val = _get_maze_at_pos(old_maze, pos)
    _set_maze_at_post(new_maze, pos, val)
    updated_count = 0
    if _get_maze_at_pos(old_maze, pos) == WALL:
        return _revel_in_1_pos(new_maze, old_maze, pos)
    if pos[0] > 0:
        updated_count += _revel_in_1_pos(new_maze,
                                         old_maze, [pos[0] - 1, pos[1]])
    if pos[1] > 0:
        updated_count += _revel_in_1_pos(new_maze,
                                         old_maze, [pos[0], pos[1] - 1])
    if pos[0] < len(new_maze) - 1:
        updated_count += _revel_in_1_pos(new_maze,
                                         old_maze, [pos[0] + 1, pos[1]])
    if pos[1] < len(new_maze) - 1:
        updated_count += _revel_in_1_pos(new_maze,
                                         old_maze, [pos[0], pos[1] + 1])
    return updated_count


def look_left(maze: np.array, full_maze: np.array, pos: (int, int)):
    current_pos = np.copy(pos)
    current_pos[0] -= 1
    updated_count = 0
    try:
        current_val = _get_maze_at_pos(maze, current_pos)
    except ValueError:
        return 0
    while current_val == UNSEEN or current_val == OPEN:
        if current_pos[0] < 0:
            break
        if _get_maze_at_pos(full_maze, current_pos) == WALL:
            updated_count += _revel_in_1_pos(maze, full_maze, current_pos)
            break
        updated_count += _revel_in_pos(maze, full_maze, current_pos)
        current_pos[0] -= 1
    return updated_count


def look_right(maze: np.array, full_maze: np.array, pos: (int, int)):
    current_pos = np.copy(pos)
    current_pos[0] += 1
    updated_count = 0
    try:
        current_val = _get_maze_at_pos(maze, current_pos)
    except ValueError:
        return 0
    while current_val == UNSEEN or current_val == OPEN:
        if current_pos[0] >= len(maze):
            break
        if _get_maze_at_pos(full_maze, current_pos) == WALL:
            updated_count += _revel_in_1_pos(maze, full_maze, current_pos)
            break
        updated_count += _revel_in_pos(maze, full_maze, current_pos)
        current_pos[0] += 1
    return updated_count


def look_up(maze: np.array, full_maze: np.array, pos: [int, int]):
    current_pos = np.copy(pos)
    current_pos[1] -= 1  # go one down
    updated_count = 0
    try:
        current_val = _get_maze_at_pos(maze, current_pos)
    except ValueError:
        return 0
    while current_val == UNSEEN or current_val == OPEN:
        if current_pos[1] < 0:
            break
        if _get_maze_at_pos(full_maze, current_pos) == WALL:
            updated_count += _revel_in_1_pos(maze, full_maze, current_pos)
            break
        updated_count += _revel_in_pos(maze, full_maze, current_pos)
        current_pos[1] -= 1
    return updated_count


def look_down(maze: np.array, full_maze: np.array, pos: [int, int]):
    current_pos = np.copy(pos)
    current_pos[1] += 1  # go one down
    updated_count = 0
    try:
        current_val = _get_maze_at_pos(maze, current_pos)
    except ValueError:
        return 0
    while current_val == UNSEEN or current_val == OPEN:
        if current_pos[1] >= len(maze):
            break
        if _get_maze_at_pos(full_maze, current_pos) == WALL:
            updated_count += _revel_in_1_pos(maze, full_maze, current_pos)
            break
        updated_count += _revel_in_pos(maze, full_maze, current_pos)
        current_pos[1] += 1
    return updated_count


def is_surrounded(maze: np.array, pos):
    up = [pos[0] - 1, pos[1]]
    down = [pos[0] + 1, pos[1]]
    left = [pos[0], pos[1] - 1]
    right = [pos[0], pos[1] + 1]
    try:
        if (_get_maze_at_pos(maze, up) == WALL and
                _get_maze_at_pos(maze, down) == WALL and
                _get_maze_at_pos(maze, left) == WALL):
            return (0, 1)
        if (_get_maze_at_pos(maze, up) == WALL and
                _get_maze_at_pos(maze, down) == WALL and
                _get_maze_at_pos(maze, right) == WALL):
            return (0, -1)
        if (_get_maze_at_pos(maze, up) == WALL and
                _get_maze_at_pos(maze, left) == WALL and
                _get_maze_at_pos(maze, right) == WALL):
            return (1, 0)
        if (_get_maze_at_pos(maze, left) == WALL and
                _get_maze_at_pos(maze, down) == WALL and
                _get_maze_at_pos(maze, right) == WALL):
            return (-1, 0)
        return None
    except ValueError:
        return None


def is_dead_end_down(maze, pos, res=False):
    val = _get_maze_at_pos(maze, pos)
    if val is None:
        return res
    if val == WALL:
        return res
    if val is OPEN:
        left_pos = [pos[0] - 1, pos[1]]
        right_pos = [pos[0] + 1, pos[1]]
        left_val = _get_maze_at_pos(maze, left_pos)
        right_val = _get_maze_at_pos(maze, right_pos)
        if left_val == OPEN or right_val == OPEN:
            return True
        return is_dead_end_down(maze, [pos[0] + 1, pos[1]], res)


def is_dead_end_up(maze, pos, res=False):
    val = _get_maze_at_pos(maze, pos)
    if val is None:
        return res
    if val == WALL:
        return res
    if val is OPEN:
        left_pos = [pos[0] - 1, pos[1]]
        right_pos = [pos[0] + 1, pos[1]]
        left_val = _get_maze_at_pos(maze, left_pos)
        right_val = _get_maze_at_pos(maze, right_pos)
        if left_val == OPEN or right_val == OPEN:
            return True
        return is_dead_end_down(maze, [pos[0] - 1, pos[1]], res)


def is_dead_end_right(maze, pos, res=False):
    val = _get_maze_at_pos(maze, pos)
    if val is None:
        return res
    if val == WALL:
        return res
    if val is OPEN:
        down_pos = [pos[0], pos[1] - 1]
        up_pos = [pos[0] + 1, pos[1] + 1]
        down_val = _get_maze_at_pos(maze, down_pos)
        up_val = _get_maze_at_pos(maze, up_pos)
        if down_val == OPEN or up_val == OPEN:
            return True
        return is_dead_end_down(maze, [pos[0], pos[1] + 1], res)


def is_dead_end_left(maze, pos, res=False):
    val = _get_maze_at_pos(maze, pos)
    if val is None:
        return res
    if val == WALL:
        return res
    if val is OPEN:
        down_pos = [pos[0], pos[1] - 1]
        up_pos = [pos[0] + 1, pos[1] + 1]
        down_val = _get_maze_at_pos(maze, down_pos)
        up_val = _get_maze_at_pos(maze, up_pos)
        if down_val == OPEN or up_val == OPEN:
            return True
        return is_dead_end_down(maze, [pos[0], pos[1] - 1], res)


def dist_from_end(maze, pos):
    maze_size = len(maze)
    dx = maze_size - 1 - pos[1]
    dy = maze_size - 1 - pos[0]
    dx = dx ^ 2
    dy = dy ^ 2
    res = sqrt(dx + dy)
    return res


def angle_from_end(maze, pos):
    maze_size = len(maze)
    dx = abs(maze_size - 1 - pos[1])
    dy = abs(maze_size - 1 - pos[0])
    res = math.atan(dy / (dx+1e-10))
    return res


def end_near_indicitor(maze, pos):
    features = np.zeros((4,))
    for i, d in enumerate([(1, 0), (-1, 0), (0, -1), (0, 1)]):
        if (pos[0]+d[0] < maze.shape[0] and pos[0]+d[0] >= 0 and
                pos[1]+d[1] >= 0 and pos[1]+d[1] < maze.shape[1]):
            end = 1 if maze[pos[0]+d[0], pos[1]+d[1]] == END else 0
            features[i] = end
        else:
            features[i] = 0
    return features


def update_maze(current_maze: np.array, full_maze: np.array,
                new_pos: [int, int], old_pos: [int, int]):
    updated_count = 0
    updated_count += _revel_in_pos(current_maze, full_maze, old_pos)
    current_maze = _set_maze_at_post(current_maze, new_pos, USER_POS)
    updated_count += look_down(current_maze, full_maze, new_pos)
    updated_count += look_right(current_maze, full_maze, new_pos)
    updated_count += look_left(current_maze, full_maze, new_pos)
    updated_count += look_up(current_maze, full_maze, new_pos)
    current_maze[new_pos[0]][new_pos[1]] = USER_POS
    current_maze[old_pos[0]][old_pos[1]] = VISITED_POS
    return updated_count


def make_maze(size, seed):
    real_maze = Maze(*size)
    init_random(seed)
    Maze.create_perfect2(real_maze, nEntrancePos=0)
    known_maze = np.ndarray(shape=(size[0], size[1]), dtype=int)
    known_maze.fill(UNSEEN)
    # m = Maze.create_perfect(maze, nEntrancePos=0, nRndBias=2)
    full_maze = np.array(list(real_maze))
    full_maze[0, 0] = OPEN
    size = size[0]
    full_maze[size-1, size-1] = END
    full_maze[size - 2, size - 1] = OPEN
    full_maze[size - 1, size - 2] = OPEN
    update_maze(known_maze, full_maze,
                [0, 0],
                [0, 0])
    # makr_entrance(arr, real_maze.entrance)
    return known_maze, full_maze


def make_maze_from_file(index):
    m = np.load('mazes_creator//mazes.npy')
    known, full = m[index]
    return known, full


def get_up(pos):
    return [pos[0] - 1, pos[1]]


def get_down(pos):
    return [pos[0] + 1, pos[1]]


def get_left(pos):
    return [pos[0], pos[1] - 1]


def get_right(pos):
    return [pos[0], pos[1] + 1]


def get_lsm_features(maze, pos):
    directions_vals = [
        _get_maze_at_pos(maze, get_down(pos)),
        _get_maze_at_pos(maze, get_up(pos)),
        _get_maze_at_pos(maze, get_left(pos)),
        _get_maze_at_pos(maze, get_right(pos))
    ]
    # print(directions_vals)
    res = []
    for p in directions_vals:
        if p == OPEN or p >= VISITED_POS:
            res.append(1)
        else:
            res.append(0)
    dist = dist_from_end(maze, pos)
    angle = angle_from_end(maze, pos)
    res.append(dist)
    res.append(angle)
    res = np.array(res)
    return res


def show_maze(maze):
    print('Maze entrance: {}'.format(maze.entrance))
    print('Maze exit: {}'.format(maze.exit))
    a = np.array(list(maze))
    plt.imshow(-a)
    plt.show()
    pass


if __name__ == '__main__':
    mazes = []
    # m = np.load('mazes.npy')
    pass
    for i in range(100):
        known, full = make_maze((15, 15), i)
        # np.save
        # np.save(f'{i}_{known}.npy',)
        mazes.append((known, full))

    np.save('mazes', mazes)
