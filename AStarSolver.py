import heapq

class AStarSolver:
    def __init__(self, maze):
        self.maze = maze
        self.start = maze.start
        self.end = maze.end
        self.path = []

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, position):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for d in directions:
            nx, ny = position[0] + d[0], position[1] + d[1]
            if 0 <= nx < self.maze.rows and 0 <= ny < self.maze.cols:
                if not self.maze.is_wall((nx, ny)):
                    neighbors.append((nx, ny))
        return neighbors

    def solve(self):
        start = self.start
        goal = self.end

        open_set = []
        heapq.heappush(open_set, (0 + self.heuristic(start, goal), 0, start, []))
        visited = set()

        while open_set:
            est_total, cost_so_far, current, path = heapq.heappop(open_set)

            if current in visited:
                continue
            visited.add(current)

            new_path = path + [current]

            if current == goal:
                self.path = new_path
                return new_path

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    new_cost = cost_so_far + 1
                    est_total = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (est_total, new_cost, neighbor, new_path))

        return []

    def get_path(self):
        return self.path
