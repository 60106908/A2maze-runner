
from Ctasks import run_explorer
from time import sleep
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("--type", choices=["random", "static"], default="random")
    parser.add_argument("--width", type=int, default=30)
    parser.add_argument("--height", type=int, default=30)
    parser.add_argument("--num_explorers", type=int, default=4)
    args = parser.parse_args()

    print(f"Launching {args.num_explorers} explorers using Celery...")

    # Launch tasks
    results = []
    for i in range(args.num_explorers):
        result = run_explorer.delay(i, args.type, args.width, args.height)
        results.append(result)

    print("Waiting for results...\n")
    # Wait for all tasks to finish
    final_results = []
    while any(not r.ready() for r in results):
        sleep(0.5)

    for r in results:
        final_results.append(r.get())

    # Print results
    print("=== Maze Exploration Summary ===")
    for r in final_results:
        print(f"Explorer {r['explorer']} -> Moves: {r['moves']} | Time: {r['time_taken']:.2f}s")

    # Find best
    best = min(final_results, key=lambda x: (x["time_taken"], x["moves"]))
    print("\n--- Best Result ---")
    print(f"Explorer {best['explorer']} with {best['moves']} moves in {best['time_taken']:.2f} seconds")
    if args.type == "static":
        print("Note: Width and height arguments were ignored for the static maze.")

if __name__ == "__main__":
    main()

