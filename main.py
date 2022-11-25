import random
import gym # https://github.com/aigagror/GymGo
from gym_go import gogame
from go_ai.player import Player
from go_ai.mcts.rollout_agents import score_agent, influence_agent, combined_score_and_influence_agent, div_by_group, combined_stones_and_influence_agent
from go_ai.mcts.tree_policies import width_first, negative_width_first

# Game variables
renderer = 'terminal'           # 'terminal' or 'human'
boardsize = 5                   # From task: 5x5 or 7x7
komi = 2.5                      # Standard komi is 7.5 points under the Chinese rules (https://en.wikipedia.org/wiki/Komi_(Go)) for 19x19 boards.
reward_method = 'heuristic'     # The reward is black 'area - white area'. If black won, the reward is 'BOARD_SIZE**2'. If white won, the reward is '-BOARD_SIZE**2'. If tied, the reward is '0'.
player = 1                      # 1 = play against the AI. 0 = let the machine play against itself.

# Initialize environment
env = gym.make('gym_go:go-v0', size=boardsize, komi=komi, reward_method=reward_method)
env.reset()

# Setup game
state = gogame.init_state(boardsize)    # Initial boardstate (empty)
black_player = Player('b', combined_stones_and_influence_agent, [1.5,1,'b'], 10_000, width_first, komi)
white_player = Player('w', combined_score_and_influence_agent, [1.5,1], 10_000, width_first, komi)

def player_move():
    """Prompts player to input coordinates for next move. Returns value for env.step()."""
    print("Enter next move:")
    player_move_x = input("x: ")
    player_move_y = input("y: ")
    return (int(player_move_y),int(player_move_x))

# Run game
done = 0
if not player:
    # Run two AIs against eachother until done
    while not done:
        state, reward, done, info = env.step(black_player.move(state))
        env.render(renderer)
        if done:
            break
        state, reward, done, info = env.step(white_player.move(state))
        env.render(renderer)

else:
    # Randomize color
    if random.randrange(2):
        while not done:
            # AI turn
            state, reward, done, info = env.step(black_player.move(state))
            env.render(renderer)
            if done:
                break
            # Player turn
            state, reward, done, info = env.step(player_move())
            env.render(renderer)
    else:
        while not done:
            # Print board to make it easier to place first stone
            env.render(renderer)
            # Player turn
            state, reward, done, info = env.step(player_move())
            env.render(renderer)
            if done:
                break
            # AI turn
            state, reward, done, info = env.step(white_player.move(state))
            env.render(renderer)