from algo.algo import MazeSolver
from helper import command_generator
from consts import Direction
import time
import json

# Initialize MazeSolver object with robot size of 20x20, center of robot at (1,1), facing north, and whether to use a big turn or not.
maze_solver = MazeSolver(40, 40, 2, 2, Direction.NORTH)
maze_solver.add_obstacle(6, 6, Direction.NORTH, 1)
maze_solver.add_obstacle(
    14,
    14,
    Direction.NORTH,
    2,
)
maze_solver.add_obstacle(
    22,
    22,
    Direction.NORTH,
    3,
)
maze_solver.add_obstacle(
    30,
    30,
    Direction.NORTH,
    4,
)
maze_solver.add_obstacle(
    14,
    30,
    Direction.WEST,
    5,
)
maze_solver.add_obstacle(
    30,
    14,
    Direction.WEST,
    6,
)
maze_solver.add_obstacle(
    6,
    22,
    Direction.WEST,
    7,
)
maze_solver.add_obstacle(
    16,
    6,
    Direction.WEST,
    8,
)


start = time.time()
# Get shortest path
obstacles = [
    {
        "x": 6,
        "y": 6,
        "id": 1,
        "d": 0,
    },
    {
        "x": 14,
        "y": 14,
        "id": 2,
        "d": 0,
    },
    {
        "x": 22,
        "y": 22,
        "id": 3,
        "d": 0,
    },
    {
        "x": 30,
        "y": 30,
        "id": 4,
        "d": 0,
    },
    {
        "x": 14,
        "y": 30,
        "id": 5,
        "d": 0,
    },
    {
        "x": 30,
        "y": 14,
        "id": 6,
        "d": 0,
    },
    {
        "x": 6,
        "y": 22,
        "id": 7,
        "d": 0,
    },
    {
        "x": 16,
        "y": 6,
        "id": 8,
        "d": 4,
    },
]
optimal_path, distance = maze_solver.get_optimal_order_dp(retrying=False)
print(f"Time taken to find shortest path using A* search: {time.time() - start}s")
print(f"Distance to travel: {distance} units")

print(f"Optimal path: {optimal_path}")
# Based on the shortest path, generate commands for the robot
commands = command_generator(optimal_path, obstacles)
print(f"Commands: {commands}")
# Get the starting location and add it to path_results
path_results = [optimal_path[0].get_dict()]

result_json_string = json.dumps(
    {
        "data": {"distance": distance, "commands": commands},
        "error": None,
    }
)
print(f"result json string: {result_json_string} type: {type(result_json_string)}")
