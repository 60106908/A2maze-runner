from collections import deque

# Classic right-hand wall following algorithm (original)
def right_hand_solver(grid, start, goal):
    # This function follows walls on the right side.
    # It does not use memory and may loop inefficiently in open spaces.
    path = []
    visited = set()
    stack = [(start, (0, 1))]  # Facing right by default

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    while stack:
        (x, y), direction = stack.pop()
        if (x, y) == goal:
            path.append((x, y))
            break
        if (x, y) in visited:
            continue
        visited.add((x, y))
        path.append((x, y))

        # Try directions in order: right turn, straight, left turn, back
        idx = directions.index(direction)
        for i in [1, 0, -1, 2]:
            new_dir = directions[(idx + i) % 4]
            nx, ny = x + new_dir[0], y + new_dir[1]
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != "#":
                stack.append(((nx, ny), new_dir))
                break

    return path

# Right-hand solver with memory to avoid revisiting
def right_hand_solver_with_memory(grid, start, goal):
    # Same as right-hand, but avoids revisiting same cells
    path = []
    visited = set()
    stack = [(start, (0, 1))]

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while stack:
        (x, y), direction = stack.pop()
        if (x, y) == goal:
            path.append((x, y))
            break
        if (x, y) in visited:
            continue
        visited.add((x, y))
        path.append((x, y))

        idx = directions.index(direction)
        for i in [1, 0, -1, 2]:
            new_dir = directions[(idx + i) % 4]
            nx, ny = x + new_dir[0], y + new_dir[1]
            if (
                0 <= nx < len(grid)
                and 0 <= ny < len(grid[0])
                and grid[nx][ny] != "#"
                and (nx, ny) not in visited
            ):
                stack.append(((nx, ny), new_dir))
                break

    return path

# Breadth-first search (guarantees shortest path in unweighted grid)
def bfs_solver(grid, start, goal):
    # More efficient pathfinding than wall-following algorithms
    queue = deque()
    queue.append((start, [start]))
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < len(grid)
                and 0 <= ny < len(grid[0])
                and grid[nx][ny] != "#"
                and (nx, ny) not in visited
            ):
                queue.append(((nx, ny), path + [(nx, ny)]))

    return []
