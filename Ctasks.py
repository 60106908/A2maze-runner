from celery import Celery
from src.maze import create_maze
from src.explorer import Explorer

app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')


@app.task
def run_explorer(index, maze_type, width, height):
    maze = create_maze(width, height, maze_type)
    explorer = Explorer(maze, visualize=False)
    time_taken, moves = explorer.solve()
    return {
        "explorer": index,
        "moves": len(moves),
        "time_taken": time_taken
    }
