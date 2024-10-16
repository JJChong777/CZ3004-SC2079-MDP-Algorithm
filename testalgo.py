from algo.algo import MazeSolver
from helper import command_generator
from consts import Direction
import time
import json

# Initialize MazeSolver object with robot size of 20x20, bottom left corner of robot at (1,1), facing north, and whether to use a big turn or not.
maze_solver = MazeSolver(20, 20, 1, 1, Direction.NORTH)
maze_solver.add_obstacle(3, 3, Direction.NORTH, 1)
maze_solver.add_obstacle(
    7,
    7,
    Direction.NORTH,
    2,
)
maze_solver.add_obstacle(
    11,
    11,
    Direction.NORTH,
    3,
)
maze_solver.add_obstacle(
    15,
    15,
    Direction.NORTH,
    4,
)
maze_solver.add_obstacle(
    7,
    15,
    Direction.WEST,
    5,
)
maze_solver.add_obstacle(
    15,
    7,
    Direction.WEST,
    6,
)
maze_solver.add_obstacle(
    3,
    11,
    Direction.WEST,
    7,
)
maze_solver.add_obstacle(
    8,
    3,
    Direction.WEST,
    8,
)


start = time.time()
# Get shortest path
obstacles = [
    {
        "x": 3,
        "y": 3,
        "id": 1,
        "d": 0,
    },
    {
        "x": 7,
        "y": 7,
        "id": 2,
        "d": 0,
    },
    {
        "x": 11,
        "y": 11,
        "id": 3,
        "d": 0,
    },
    {
        "x": 15,
        "y": 15,
        "id": 4,
        "d": 0,
    },
    {
        "x": 7,
        "y": 15,
        "id": 5,
        "d": 0,
    },
    {
        "x": 15,
        "y": 7,
        "id": 6,
        "d": 0,
    },
    {
        "x": 3,
        "y": 11,
        "id": 7,
        "d": 0,
    },
    {
        "x": 8,
        "y": 3,
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
