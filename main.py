import gym # https://github.com/aigagror/GymGo
from gym_go import gogame
from go_ai.player import Player
from go_ai.mcts import rollout_agents

# Game variables
renderer = 'terminal'           # 'terminal' or 'human'
boardsize = 5                   # From task: 5x5 or 7x7
komi = 2.5                      # Standard komi is 7.5 points under the Chinese rules (https://en.wikipedia.org/wiki/Komi_(Go))
reward_method = 'heuristic'     # The reward is black 'area - white area'. If black won, the reward is 'BOARD_SIZE**2'. If white won, the reward is '-BOARD_SIZE**2'. If tied, the reward is '0'.

# Initialize environment
env = gym.make('gym_go:go-v0', size=boardsize, komi=komi, reward_method=reward_method)
env.reset()

# Setup game
state = gogame.init_state(boardsize)    # Initial boardstate (empty)
black_player = Player('b', rollout_agents.rand_agent, [10], 3, komi)
white_player = Player('w', rollout_agents.rand_agent, [10], 3, komi)

# Run game
done = 0
while not done:
    state, reward, done, info = env.step(black_player.move(state))
    env.render(renderer)
    if done:
        break
    state, reward, done, info = env.step(white_player.move(state))
    env.render(renderer)