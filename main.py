import gym
from gym_go import gogame


go_env = gym.make('gym_go:go-v0', size=5, komi=0, reward_method='real')
go_env.reset()

first_action = (0, 4)
second_action = (0, 0)
state, reward, done, info = go_env.step(first_action)

go_env.step(gogame.random_action(state))


go_env.render('terminal')
