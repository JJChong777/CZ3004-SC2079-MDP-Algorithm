from algo.algo import MazeSolver
from helper import command_generator
from consts import Direction
import time
import json

# Initialize MazeSolver object with robot size of 20x20, bottom left corner of robot at (1,1), facing north, and whether to use a big turn or not.
maze_solver = MazeSolver(20, 20, 1, 1, Direction.NORTH)
maze_solver.add_obstacle(
    7,
    7,
    Direction.NORTH,
    1,
)
maze_solver.add_obstacle(
    11,
    11,
    Direction.NORTH,
    2,
)


start = time.time()
# Get shortest path
obstacles = [
    {
        "x": 7,
        "y": 7,
        "id": 1,
        "d": 0,
    },
    {
        "x": 11,
        "y": 11,
        "id": 2,
        "d": 0,
    },
]
optimal_path, distance = maze_solver.get_optimal_order_dp(retrying=False)
print(f"Time taken to find shortest path using A* search: {time.time() - start}s")
print(f"Distance to travel: {distance} units")

print(f"Optimal path: {optimal_path}")
# Based on the shortest path, generate commands for the robot
commands = command_generator(optimal_path, obstacles)
print(f"Commands: {commands}")
commands_string = ",".join(commands)
enum_to_label = {0: "N", 2: "E", 4: "S", 6: "W"}
path_results = []
# Process each command individually and append the location the robot should be after executing that command to path_results
i = 0
for command in commands:
    if command.startswith("SP"):
        path_results.append(
            f"{optimal_path[i].get_dict()["x"]},{optimal_path[i].get_dict()["y"]},{enum_to_label[optimal_path[i].get_dict()["d"]]}"
        )
        continue
    elif command.startswith("FW"):
        i += int(command[2:]) // 10
    elif command.startswith("BW"):
        i += int(command[2:]) // 10
    else:
        i += 1
    # print(i)
    path_results.append(
        f"{optimal_path[i].get_dict()["x"]},{optimal_path[i].get_dict()["y"]},{enum_to_label[optimal_path[i].get_dict()["d"]]}"
    )
path_results = ";".join(path_results)
print(path_results)
# print(f"len(commands): {len(commands)}")
# print(f"len(coords): {len(path_results)}")
# print(f"length equal: {len(commands) == len(path_results)}")
