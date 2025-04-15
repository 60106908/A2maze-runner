from collections import deque

def bfs_solver(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    prev = [[None for _ in range(cols)] for _ in range(rows)]

    queue = deque()
    queue.append(start)
    visited[start[0]][start[1]] = True

    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            break

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != 1 and not visited[nr][nc]:
                queue.append((nr, nc))
                visited[nr][nc] = True
                prev[nr][nc] = (r, c)

    # Reconstruct path
    path = []
    at = goal
    while at != start:
        path.append(at)
        at = prev[at[0]][at[1]]
        if at is None:  # No path found
            return []

    path.append(start)
    path.reverse()
    return path
