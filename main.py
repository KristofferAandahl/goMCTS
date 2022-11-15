import gym
from gym_go import gogame
import MCTS


go_env = gym.make('gym_go:go-v0', size=5, komi=0, reward_method='real')
go_env.reset()

state, reward, done, info = go_env.step((1, 1))

for i in range(25):
    state, reward, done, info = go_env.step(MCTS.move(state, 'w').parent_action)
    if done:
        break
    state, reward, done, info = go_env.step(MCTS.move(state, 'b').parent_action)
    if done:
        break
    go_env.render('human')

go_env.render('human')

