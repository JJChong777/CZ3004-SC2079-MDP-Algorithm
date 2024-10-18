import socket
from algo.algo import MazeSolver
from helper import command_generator
from consts import Direction
import json

PORT = 50000
CLIENT_ADDR = "192.168.8.8"
CLIENT_NAME = f"pi@{CLIENT_ADDR}"

s = socket.socket()
s.bind(("", PORT))
s.listen(1)

while True:
    print("Waiting for client connection...")
    c, addr = s.accept()
    if addr[0] != CLIENT_ADDR:
        print(f"Client addr not equal to {CLIENT_ADDR}: {addr[0]}")
        c.close()
        break
    print("Accepted connection from", addr)
    content = c.recv(1024).decode()
    content = json.loads(content)
    # content = {
    #     "type": "START_TASK",
    #     "data": {
    #         "task": "EXPLORATION",
    #         "robot": {"id": "R", "x": 1, "y": 1, "dir": "N"},
    #         "obstacles": [
    #             {"id": "1", "x": 4, "y": 4, "dir": "N"},
    #             {"id": "2", "x": 7, "y": 7, "dir": "N"},
    #             {"id": "3", "x": 11, "y": 11, "dir": "N"},
    #             {"id": "4", "x": 15, "y": 15, "dir": "N"},
    #             {"id": "5", "x": 7, "y": 15, "dir": "N"},
    #             {"id": "6", "x": 15, "y": 7, "dir": "N"},
    #             {"id": "7", "x": 3, "y": 11, "dir": "N"},
    #             {"id": "8", "x": 8, "y": 3, "dir": "S"},
    #         ],
    #     },
    # }
    label_to_enum = {
        "N": Direction.NORTH,
        "S": Direction.SOUTH,
        "W": Direction.WEST,
        "E": Direction.EAST,
    }
    env_data = content["data"]
    robot_info = env_data["robot"]
    robot_x = robot_info["x"]
    robot_y = robot_info["y"]
    robot_direction = label_to_enum[robot_info["dir"]]
    # Initialize MazeSolver object with robot size of 20x20, bottom left corner of robot at (1,1), facing north, and whether to use a big turn or not.
    maze_solver = MazeSolver(20, 20, robot_x, robot_y, robot_direction)

    obstacles = env_data["obstacles"]
    obstacle_info = []
    for ob in obstacles:
        print(1)
        maze_solver.add_obstacle(ob["x"], ob["y"], label_to_enum[ob["dir"]], ob["id"])
        obstacle_info.append(
            {"x": ob["x"], "y": ob["y"], "id": ob["id"], "d": label_to_enum[ob["dir"]]}
        )

    optimal_path, distance = maze_solver.get_optimal_order_dp(retrying=False)
    # Based on the shortest path, generate commands for the robot
    commands = command_generator(optimal_path, obstacle_info)
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
        if command.startswith("FIN"):
            continue
        elif command.startswith("FW"):
            i += int(command[2:]) // 10
        elif command.startswith("BW"):
            i += int(command[2:]) // 10
        else:
            i += 1
        path_results.append(
            f"{optimal_path[i].get_dict()["x"]},{optimal_path[i].get_dict()["y"]},{enum_to_label[optimal_path[i].get_dict()["d"]]}"
        )

    commands_string = ",".join(commands)
    coords_string = ";".join(path_results)
    data = json.dumps({"commands_string": commands_string, "coords": coords_string})
    print(data)
    c.send(data.encode())

s.close()
