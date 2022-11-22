from go_ai.mcts import mcts

class Player:
    """
    The main class representing a color. This class kinda represents a tree and keeps some settings/information about our tree data structure.
    """
    def __init__(self, color, agent, settings, simulation_no, tree_policy, komi):
        self.color = color
        self.agent = agent
        self.settings = settings
        self.simulation_no = simulation_no
        self.tree_policy = tree_policy
        self.komi = komi

    def move(self, state):
        """
        Returns action needed for calculated best state. This move will hopefully lead to the best outcome.
        """
        root = mcts.MonteCarloTreeSearchNode(state, self.color, self.komi, self.simulation_no, self.tree_policy, self.agent, self.settings)
        selected_node = root.best_action()
        return selected_node.parent_action
