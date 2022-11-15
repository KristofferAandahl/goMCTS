import gym # https://github.com/aigagror/GymGo
import traceback
from gym_go import gogame
from player import player
from rollout_agents import rand_agent

# Game variables
renderer = 'terminal'           # 'terminal' or 'human'
boardsize = 5                   # From task: 5x5 or 7x7
komi = 0                        # Standard komi is 7.5 points under the Chinese rules (https://en.wikipedia.org/wiki/Komi_(Go))
reward_method = 'heuristic'     # The reward is black 'area - white area'. If black won, the reward is 'BOARD_SIZE**2'. If white won, the reward is '-BOARD_SIZE**2'. If tied, the reward is '0'.

# Initialize environment
env = gym.make('gym_go:go-v0', size=boardsize, komi=komi, reward_method=reward_method)
env.reset()

# Run game
done = 0
state = gogame.init_state(boardsize)    # Initial boardstate (empty)
black = player('b', rand_agent, [10], 3, komi)
white = player('w', rand_agent, [10], 3, komi)

while not done:
    try:
        state, reward, done, info = env.step(black.move(state))
        env.render(renderer)
        state, reward, done, info = env.step(white.move(state))
        env.render(renderer)
    except: 
        traceback.print_exc()
        break