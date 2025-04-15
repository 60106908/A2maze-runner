from celery import Celery
from src.maze import create_maze
from src.explorer import Explorer

# Setup Celery app with RabbitMQ as broker and Redis as backend
app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')

@app.task
def run_explorer(index, maze_type, width, height, solver="right_hand"):
    # Create the maze based on the given type and size
    maze = create_maze(width, height, maze_type)
    
    # Pass the chosen solver method to Explorer
    explorer = Explorer(maze, visualize=False, solver=solver)
    
    # Solve the maze and get performance metrics
    time_taken, moves = explorer.solve()
    
    # Return results including number of moves and time taken
    return {
        "explorer": index,
        "moves": len(moves),
        "time_taken": time_taken
    }

