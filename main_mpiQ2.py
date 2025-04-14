from mpi4py import MPI
from src.maze import create_maze
from src.explorer import Explorer
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Parallel Maze Explorer with MPI")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                        help="Maze type (random or static)")
    parser.add_argument("--width", type=int, default=30,
                        help="Width of the maze (ignored for static)")
    parser.add_argument("--height", type=int, default=30,
                        help="Height of the maze (ignored for static)")
    return parser.parse_args()

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    args = parse_arguments()

    # All processes generate the maze and solve it
    maze = create_maze(args.width, args.height, args.type)
    explorer = Explorer(maze, visualize=False)
    time_taken, moves = explorer.solve()

    result = {
        'rank': rank,
        'time': time_taken,
        'moves': len(moves)
    }

    # Gather results at rank 0
    all_results = comm.gather(result, root=0)

    if rank == 0:
        print("\n=== Maze Exploration Summary ===")
        best = min(all_results, key=lambda r: r['moves'])

        for r in all_results:
            print(f"Explorer {r['rank']} -> Moves: {r['moves']} | Time: {r['time']:.2f}s")

        print("\n--- Best Result ---")
        print(f"Explorer {best['rank']} with {best['moves']} moves in {best['time']:.2f} seconds")

        if args.type == "static":
            print("Note: Width and height arguments were ignored for the static maze.")

if __name__ == "__main__":
    main()
