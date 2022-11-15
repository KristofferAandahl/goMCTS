import MCTS

class player():
    def __init__(self, color, agent, simulation_no, komi):
        self.color = color
        self.agent = agent
        self.simulation_no = simulation_no
        self.komi = komi

    def move(self, state):
        root = MCTS.MonteCarloTreeSearchNode(state, self.color, self.komi)
        selected_node = root.best_action()
        return selected_node.parent_action