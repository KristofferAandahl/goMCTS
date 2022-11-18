from go_ai.mcts import mcts

class Player:
    def __init__(self, color, agent, settings, simulation_no, tree_policy, komi):
        self.color = color
        self.agent = agent
        self.settings = settings
        self.simulation_no = simulation_no
        self.tree_policy = tree_policy
        self.komi = komi

    def move(self, state):
        root = mcts.MonteCarloTreeSearchNode(state, self.color, self.komi, self.simulation_no, self.tree_policy, self.agent, self.settings)
        selected_node = root.best_action()
        return selected_node.parent_action