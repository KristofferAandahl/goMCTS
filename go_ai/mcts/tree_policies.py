def width_first(node):
    """Construct the path from root to most promising leaf node. A leaf node is a node which has unexplored child node(s)."""
    current_node = node

    while not current_node.is_terminal_node():
        if not current_node.is_fully_expanded():
            return current_node.expand()
        else:
            current_node = current_node.best_child()

    return current_node


def negative_width_first(node):
    """Construct the path from root to most promising leaf node. A leaf node is a node which has unexplored child node(s)."""
    current_node = node
    dept = 0

    while not current_node.is_terminal_node():
        dept += 1
        if not current_node.is_fully_expanded():
            return current_node.expand()
        else:
            if dept % 2 == 1:
                current_node = current_node.best_child()
            else:
                current_node = current_node.worst_child()

    return current_node
