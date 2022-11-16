import numpy as np
from gym_go import gogame
from collections import defaultdict

class MonteCarloTreeSearchNode():
    """
    Class representing a node in the Monte Carlo Tree Search for Go.

    Monte Carlo Tree Search (MCTS) is a search technique in the field of Artificial Intelligence (AI). It is a probabilistic and heuristic driven search algorithm that combines the classic tree search implementations alongside machine learning principles of reinforcement learning. In MCTS, nodes are the building blocks of the search tree. These nodes are formed based on the outcome of a number of simulations. The process of MCTS can be broken down into four distinct steps: selection, expansion, simulation and backpropagation.
    """

    def __init__(self, state, color:str, komi:int, simulation_no:int, agent, settings:list, parent=None, parent_action=None):
        self.state = state
        if color not in {'b', 'w'}:
            raise ValueError("color must be 'b' or 'w'")
        self.color = color
        self.settings = settings
        self.komi = komi
        self.simulation_no = simulation_no
        self.agent = agent
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()

    def untried_actions(self):
        """Returns a List over all valid moves that it not yet visited. Used when expanding the tree."""
        self._untried_actions = list(gogame.valid_moves(self.state))
        return self._untried_actions

    def n(self):
        """Returns the number of times the node has been visited."""
        return self._number_of_visits

    def q(self):
        """Returns number of wins more than opponent."""
        black = self._results[1]    # results[1] is number of black wins
        white = self._results[-1]   # results[-1] is black losses

        if self.color == 'b':
            return black - white
        else:
            return white - black

    def expand(self):
        """Creates a new node based on a random move. Updates untried_actions. Returns new child node."""
        action = gogame.random_action(self.state)

        while self._untried_actions[action] == 0:
            action = gogame.random_action(self.state)

        self._untried_actions[action] = 0
        next_state = gogame.next_state(self.state, action)

        child_node = MonteCarloTreeSearchNode(
            next_state, 
            self.color, 
            self.komi,  
            self.simulation_no, 
            self.agent, 
            self.settings, 
            parent=self, 
            parent_action=action
        )

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        """Checks if game has ended (e.g. win/loss/draw)."""
        return gogame.game_ended(self.state)

    def rollout(self):
        """Completes one playout from current node based on agent. Does not save the moves, but checks for a winner at the end of the playout."""
        return self.agent(self.state, self.komi, self.settings)

    def backpropagate(self, result):
        """Use the result of the rollout to update information in nodes on the current branch."""
        self._number_of_visits += 1
        self._results[np.sign(result)] += abs(result)

        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        """Unless the game ends decisively (e.g. win/loss/draw) for either player, create one (or more) child nodes. Child nodes are any valid moves from the game position defined by current leaf node."""
        expand = 0
        for action in self._untried_actions:
            expand += action

        return (expand == 0)

    def best_child(self, c_param=0.1):
        """Selects the node with the highest estimated value. Uses the Upper Confidence Bound (UCB) formula for node values."""
        # TODO: Er dette UCB eller en annen variant? 
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def _tree_policy(self):
        """Construct the path from root to most promising leaf node. A leaf node is a node which has unexplored child node(s)."""
        current_node = self

        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        
        return current_node

    def best_action(self):
        """Selects best action based on branch with most calculated value."""
        for _ in range(self.simulation_no):
            v = self._tree_policy()
            v.backpropagate(v.rollout())

        return self.best_child(c_param=0.)
