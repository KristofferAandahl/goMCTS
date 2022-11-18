def width_first(node):
    """Construct the path from root to most promising leaf node. A leaf node is a node which has unexplored child node(s)."""
    current_node = node

    while not current_node.is_terminal_node():
        if not current_node.is_fully_expanded():
            return current_node.expand()
        else:
            current_node = current_node.best_child()

    return current_node