import matplotlib.pyplot as plt
import numpy as np
from daedalus import Maze
from .maze_consts import WALL,USER_POS, OPEN, UNSEEN


def _get_maze_at_pos(maze: np.array, pos: (int, int)):
    return maze[pos[0]][pos[1]]


def _set_maze_at_post(maze: np.array, pos: (int, int), val: int):
    maze[pos[0]][pos[1]] = val
    return maze


def _revel_in_1_pos(new_maze, old_maze, pos):
    val = _get_maze_at_pos(old_maze, pos)
    maze = _set_maze_at_post(new_maze, pos, val)
    return maze
def _revel_in_pos(new_maze, old_maze, pos):
    val = _get_maze_at_pos(old_maze, pos)
    maze = _set_maze_at_post(new_maze, pos, val)
    if pos[0]>0:
        _revel_in_1_pos(new_maze,old_maze,[pos[0]-1,pos[1]])
    if pos[1]>0:
        _revel_in_1_pos(new_maze,old_maze,[pos[0],pos[1]-1])
    if pos[0]<len(new_maze)-1:
        _revel_in_1_pos(new_maze,old_maze,[pos[0]+1,pos[1]])
    if pos[1]<len(new_maze)-1:
        _revel_in_1_pos(new_maze,old_maze,[pos[0],pos[1]+1])
    return maze

def look_left(maze: np.array, full_maze: np.array, pos: (int, int)):
    current_pos = np.copy(pos)
    current_pos[0] -= 1
    current_val = _get_maze_at_pos(maze, current_pos)
    while current_val != UNSEEN:
        if current_pos[0] <0:
            break
        if _get_maze_at_pos(full_maze,current_pos)==WALL:
            maze = _revel_in_pos(maze, full_maze, current_pos)
            break
        maze = _revel_in_pos(maze, full_maze, current_pos)
        current_pos[0] -= 1
    return maze
def look_right(maze: np.array, full_maze: np.array, pos: (int, int)):
    current_pos = np.copy(pos)
    current_pos[0] += 1
    current_val = _get_maze_at_pos(maze, current_pos)
    while current_val != UNSEEN:
        if current_pos[0] >= len(maze):
            break
        if _get_maze_at_pos(full_maze,current_pos)==WALL:
            maze = _revel_in_pos(maze, full_maze, current_pos)
            break
        maze = _revel_in_pos(maze, full_maze, current_pos)
        current_pos[0] += 1
    return maze

def look_up(maze: np.array, full_maze: np.array, pos: [int, int]):
    current_pos = np.copy(pos)
    current_pos[1] -= 1  # go one down
    current_val = _get_maze_at_pos(maze, current_pos)
    while current_val == UNSEEN:
        if current_pos[1] < 0:
            break
        if _get_maze_at_pos(full_maze,current_pos)==WALL:
            maze = _revel_in_pos(maze, full_maze, current_pos)
            break
        maze = _revel_in_pos(maze, full_maze, current_pos)
        current_pos[1] -= 1
    return maze

def look_down(maze: np.array, full_maze: np.array, pos: [int, int]):
    current_pos = np.copy(pos)
    current_pos[1] += 1  # go one down
    current_val = _get_maze_at_pos(maze, current_pos)
    while current_val == UNSEEN:
        if current_pos[1] >= len(maze):
            break
        if _get_maze_at_pos(full_maze,current_pos)==WALL:
            maze = _revel_in_pos(maze, full_maze, current_pos)
            break
        maze = _revel_in_pos(maze, full_maze, current_pos)
        current_pos[1] += 1
    return maze


def update_maze(current_maze: np.array, full_maze: np.array,
                new_pos: [int, int], old_pos: [int, int]):
    # current_maze = _set_maze_at_post(current_maze, old_pos, _get_maze_at_pos(full_maze, old_pos))
    _revel_in_pos(current_maze, full_maze, old_pos)
    # current_maze[old_pos[0]][old_pos[1]]=_get_maze_at_pos(full_maze,old_pos)
    current_maze = _set_maze_at_post(current_maze, new_pos, USER_POS)
    look_down(current_maze,full_maze,new_pos)
    look_right(current_maze,full_maze,new_pos)
    look_left(current_maze,full_maze,new_pos)
    look_up(current_maze,full_maze,new_pos)
    # current_maze[new_pos[0]][new_pos[1]] = USER_POS


"""
1 wall
0 open
-1 unseen
999 user
"""


def make_maze(size):
    real_maze = Maze(*size)
    Maze.create_perfect(real_maze, nEntrancePos=0, nRndBias=2)
    known_maze = np.ndarray(shape=(size[0],size[1]),dtype=int)
    known_maze.fill(UNSEEN)
    # m = Maze.create_perfect(maze, nEntrancePos=0, nRndBias=2)
    arr = np.array(list(real_maze))
    update_maze(known_maze,arr,
                list(real_maze.entrance),
                list(real_maze.entrance))
    # makr_entrance(arr, real_maze.entrance)

    return arr


def show_maze(maze):
    print('Maze entrance: {}'.format(maze.entrance))
    print('Maze exit: {}'.format(maze.exit))
    a = np.array(list(maze))
    plt.imshow(-a)
    plt.show()
    pass


def main():
    SIZE = 31
    m = make_maze((SIZE, SIZE))
    show_maze(m)


if __name__ == '__main__':
    main()