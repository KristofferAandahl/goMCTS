import gym
from gym_go import gogame
import MCTS
import player


go_env = gym.make('gym_go:go-v0', size=5, komi=0, reward_method='real')
go_env.reset()
state, reward, done, info = go_env.step((1,1))

black = player.player('b', 'rand', 3, 0)
white = player.player('w', 'rand', 3, 0)

for i in range(25):
    state, reward, done, info = go_env.step(white.move(state))
    if done:
        break
    state, reward, done, info = go_env.step(black.move(state))
    if done:
        break
    go_env.render('human')
go_env.render('human')
