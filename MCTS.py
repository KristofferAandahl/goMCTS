import numpy as np
from collections import defaultdict
import gym
import rollout_agents as agents
from gym_go import gogame


class MonteCarloTreeSearchNode():
    # Color should be b or w
    def __init__(self, state, color, komi, parent=None, parent_action=None):
        self.state = state
        self.color = color
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        self.komi = komi
        return

    # A list of 1s and 0s. 1 is unvisited valid move. Used in expand to find moves to expand the tree with
    def untried_actions(self):
        self._untried_actions = list(gogame.valid_moves(self.state))
        return self._untried_actions

    def n(self):
        return self._number_of_visits

    # Method for finding nodes winrate. Result[0] is number of ties, [1] is number of wins and [-1] is losses
    def q(self):
        black = self._results[1]
        white = self._results[-1]
        if self.color == 'b':
            return black - white
        else:
            return white - black

    # Creates a new node based on a random move and updates the untried action list
    def expand(self):
        action = gogame.random_action(self.state)
        while self._untried_actions[action] == 0:
            action = gogame.random_action(self.state)

        self._untried_actions[action] = 0
        next_state = gogame.next_state(self.state, action)
        child_node = MonteCarloTreeSearchNode(
            next_state, self.color, self.komi, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    # Checks if game is finished in the current node
    def is_terminal_node(self):
        return gogame.game_ended(self.state)

    # Continues the current state with random moves, does not save the moves, but checks who won then the game
    # at the end of the rollout
    def rollout(self):
        return agents.rand_agent(self.state, self.komi, 5)

    # Updates statistics for the node and its parent chain
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    # Checks if all moves are checked in the current node
    def is_fully_expanded(self):
        expand = 0
        for i in self._untried_actions:
            expand += i
        return expand == 0

    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    # Defines how the tree comitts rollouts. Currently unused. Better policies creates a more efficient system
    def rollout_policy(self):
        possible_moves = gogame.valid_moves(self.state)
        r = np.random.randint(len(possible_moves))
        while possible_moves(r) == 0:
            r = np.random.randint(len(possible_moves))
        return r

    # Drives the tree expansion
    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        # How many moves are considered
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            v.backpropagate(v.rollout())

        return self.best_child(c_param=0.)





