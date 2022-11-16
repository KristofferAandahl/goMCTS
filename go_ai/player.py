from go_ai.mcts import MCTS

class player:
    def __init__(self, color, agent, settings, simulation_no, komi):
        self.color = color
        self.agent = agent
        self.settings = settings
        self.simulation_no = simulation_no
        self.komi = komi

    def move(self, state):
        root = MCTS.MonteCarloTreeSearchNode(state, self.color, self.komi, self.simulation_no, self.agent, self.settings)
        selected_node = root.best_action()
        return selected_node.parent_action
