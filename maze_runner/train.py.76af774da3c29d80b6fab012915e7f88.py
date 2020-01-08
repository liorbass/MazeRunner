from evostra import EvolutionStrategy
from .models.model import Model
from .mazes_creator.maze_manager import make_maze, show_maze, update_maze
from .mazes_creator.maze_consts import STRARTING_POSINGTION, WALL, MAZE_ENDING
from .consts import TESTSET_SIZE, TRAINSET_SIZE, MAZE_SIZE, MAX_STEPS


def run_maze(model, maze):
    curr_pos = np.array(STRARTING_POSINGTION)
    curr_maze = []
    score = 0
    for i in range(MAX_STEPS):
        pred = np.array(model.predict(maze))
        if np.sum(maze[curr_pos+pred] == MAZE_ENDING)==2:
            score -=1
            return score
        elif maze[curr_pos+pred] == WALL:
            score+=2
        else:
            curr_pos += pred
            score+=1
        update_maze(curr_maze, maze, curr_pos+pred, curr_pos)
    return score

def reward_func(mazes, model):
    def get_reward(weights):
        model.set_weights(weights)
        reward = 0
        for maze in mazes:
            reward += run_maze(model, maze)
        return reward / len(mazes)
    return get_reward


if __name__ == '__main__':
    mazes = [make_maze(MAZE_SIZE) for i in range(TRAINSET_SIZE)]
    model = Model(fillters_number=10, dense_size=10, img_size=28)
    es = EvolutionStrategy(model.get_weights, reward_func(mazes, model))
    es.run(iterations=100, print_step=10)