def distance(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def astar(start, end, adj_matrix, moves=-1):
    """
    A* pathfinding.

    :param tuple start: (x,y) start position.
    :param tuple end: (x,y) goal position.
    :param dict adj_matrix: adjacency matrix {(x,y): (a,b), (c,d), ...}
    :param int moves: number of grid spaces to move towards end.
                      If -1, returns the entire path.
    :returns: new_position towards end after move.
    :rtype: tuple
    """

    frontier = [start]
    came_from = {}

    while frontier != []:
        current = frontier.pop(0)
        adjacents = [n for n in adj_matrix[current] if n not in came_from]
        # If there is nowhere to go or we're adjacent to the goal,
        # stay where we are.
        if not adjacents:
            continue
        if distance(current, end) == 1:
            break
        for n in adjacents:
            came_from[n] = current
        frontier.extend(sorted(adjacents, key=lambda n: distance(end, n)))

    # reconstruct the path
    path = [current]
    while current != start:
        path.append(came_from[current])
        current = came_from[current]
    # We built it from finish to start,
    # but we report it from start to finish.
    path = path[::-1]
    if moves == -1:
        return path
    else:
        idx = min(len(path)-1, moves)
        return path[:idx+1]
