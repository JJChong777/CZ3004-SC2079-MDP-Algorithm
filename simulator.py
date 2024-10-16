import tkinter as tk
from consts import OBS_DIM, Direction, WIDTH, HEIGHT, ROBOT_X, ROBOT_Y
from algo.algo import MazeSolver
from helper import command_generator
import time


class CarSimulator:
    def __init__(self, grid_size=600, cell_size=30):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.root = tk.Tk()
        self.root.title("Car Simulator")
        self.canvas = tk.Canvas(self.root, width=grid_size, height=grid_size, bg="white")
        self.canvas.pack(side=tk.LEFT)

        # Frame for dropdown menus
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Dictionary to store obstacle rectangles by position
        self.obstacle_dict = {}
        self.car_position = None
        self.path_coords = []

        # Map direction strings to enum values
        self.dir_enum_to_label = {
            Direction.NORTH: "North",
            Direction.SOUTH: "South",
            Direction.EAST: "East",
            Direction.WEST: "West",
        }
        self.label_to_dir_enum = {v: k for k, v in self.dir_enum_to_label.items()}

        # Draw the grid
        self.draw_grid()

        # Initialize car position (default at starting point)
        self.draw_car(ROBOT_X, ROBOT_Y, Direction.NORTH)

        # Bind left mouse click to toggle obstacles
        self.canvas.bind("<Button-1>", self.toggle_obstacle)

        # Add the "Run Algo" button
        self.run_algo_button = tk.Button(self.control_frame, text="Run Algorithm", command=self.run_algo)
        self.run_algo_button.pack(side=tk.BOTTOM, anchor="se", padx=10, pady=10)

        # Add the "Reset All" button
        self.reset_button = tk.Button(self.control_frame, text="Reset All", command=self.reset_simulation)
        self.reset_button.pack(side=tk.BOTTOM, anchor="se", padx=10, pady=10)

    def draw_grid(self):
        for i in range(0, self.grid_size, self.cell_size):
            self.canvas.create_line([(i, 0), (i, self.grid_size)], tag="grid_line", fill="black")
            self.canvas.create_line([(0, i), (self.grid_size, i)], tag="grid_line", fill="black")

    def draw_car(self, x, y, direction):
        """Draw the car as a 3x3 block with the front-middle square highlighted to represent the camera, starting from the bottom-left corner."""
        
        # bottom-left corner coordinates are provided as (x, y)
        bottom_left_x = (x - 1) * self.cell_size
        bottom_left_y = self.grid_size - (y - 1) * self.cell_size
        
        car_blocks = []

        # Draw 3x3 car body starting from the bottom-left corner
        for i in range(3):
            for j in range(3):
                car_blocks.append(
                    self.canvas.create_rectangle(
                        bottom_left_x + j * self.cell_size,  # horizontal position
                        bottom_left_y - i * self.cell_size,  # vertical position
                        bottom_left_x + (j + 1) * self.cell_size,
                        bottom_left_y - (i + 1) * self.cell_size,
                        fill="gray",
                        tags="car"
                    )
                )

        # Highlight the front-middle square (camera position) based on the car's direction
        if direction == Direction.NORTH:
            car_blocks[1] = self.canvas.create_rectangle(
                bottom_left_x + self.cell_size,       
                bottom_left_y - 3 * self.cell_size,  
                bottom_left_x + 2 * self.cell_size,  
                bottom_left_y - 2 * self.cell_size,  
                fill="yellow",
                tags="car"
            )
        elif direction == Direction.SOUTH:
            car_blocks[1] = self.canvas.create_rectangle(
                bottom_left_x + self.cell_size,       
                bottom_left_y,                       
                bottom_left_x + 2 * self.cell_size,  
                bottom_left_y - self.cell_size,      
                fill="yellow",
                tags="car"
            )
        elif direction == Direction.EAST:
            car_blocks[1] = self.canvas.create_rectangle(
                bottom_left_x + 2 * self.cell_size,   
                bottom_left_y - self.cell_size,       
                bottom_left_x + 3 * self.cell_size,   
                bottom_left_y - 2 * self.cell_size,   
                fill="yellow",
                tags="car"
            )
        elif direction == Direction.WEST:
            car_blocks[1] = self.canvas.create_rectangle(
                bottom_left_x,                       
                bottom_left_y - self.cell_size,       
                bottom_left_x + self.cell_size,       
                bottom_left_y - 2 * self.cell_size,   
                fill="yellow",
                tags="car"
            )

        self.car_position = (x, y)
        return car_blocks

    def reset_simulation(self):
        """Reset the simulation by clearing the obstacles, paths, and resetting the car's position."""
        # Delete all obstacles, their images, and car elements from the canvas
        self.canvas.delete("obstacle")
        self.canvas.delete("obstacle_image")
        self.canvas.delete("car")
        self.canvas.delete("path")
        
        # Reset obstacle dictionary
        self.obstacle_dict.clear()

        # Reset the car to its initial position
        self.draw_car(ROBOT_X, ROBOT_Y, Direction.NORTH)

        # Clear control frame (dropdowns for obstacle directions)
        for widget in self.control_frame.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.OptionMenu):
                widget.destroy()


    def update_car_position(self, x, y, direction):
        """Move the car to new coordinates and update the path."""
        if self.car_position:
            prev_x, prev_y = self.car_position
            # Draw path from previous position to new position
            self.draw_path(prev_x, prev_y, x, y)

        # Clear the old car and redraw it at the new position
        self.canvas.delete("car")
        self.draw_car(x, y, direction)  # Now calling the updated draw_car function with bottom-left coordinates

    def draw_path(self, prev_x, prev_y, new_x, new_y):
        """Draw a line from the previous position to the new position."""
        self.canvas.create_line(
            prev_x * self.cell_size + 0.5 * self.cell_size,  # Center of the previous car position
            self.grid_size - prev_y * self.cell_size - 0.5 * self.cell_size,
            new_x * self.cell_size + 0.5 * self.cell_size,  # Center of the new car position
            self.grid_size - new_y * self.cell_size - 0.5 * self.cell_size,
            fill="blue", width=2, tags="path"  # Add a tag for the path
        )


    def simulate_camera_action(self, direction):
        """Simulate camera taking a picture by changing the top-middle square's color."""
        car_blocks = self.draw_car(*self.car_position, direction)
        self.canvas.itemconfig(car_blocks[1], fill="red")  # Camera indicates picture taken
        self.root.update()
        time.sleep(1)  # Pause for 1 second to take picture
        self.canvas.itemconfig(car_blocks[1], fill="yellow")

    def update_obstacle_image(self, key, img_id, direction_var):
        """Update the obstacle's image location based on the new direction."""
        self.obstacle_dict[key]["img_dir"] = self.label_to_dir_enum[direction_var.get()]
        image_dir = self.obstacle_dict[key]["img_dir"]

        # Delete the previous small image (img_id), but keep the obstacle's rectangle (rect_id)
        self.canvas.delete(img_id)

        # Calculate the new image position based on the new direction
        botleft_x, botleft_y = key
        x1, y1 = botleft_x * self.cell_size, self.grid_size - (botleft_y + OBS_DIM) * self.cell_size
        x2, y2 = (botleft_x + OBS_DIM) * self.cell_size, self.grid_size - botleft_y * self.cell_size

        if image_dir == Direction.NORTH:
            img_x1, img_y1 = x1, y1
            img_x2, img_y2 = x2, y1 + (0.2 * (y2 - y1))  # 20% height at the top
        elif image_dir == Direction.SOUTH:
            img_x1, img_y1 = x1, y2 - (0.2 * (y2 - y1))  # 20% height at the bottom
            img_x2, img_y2 = x2, y2
        elif image_dir == Direction.EAST:
            img_x1, img_y1 = x2 - (0.2 * (x2 - x1)), y1  # 20% width on the right
            img_x2, img_y2 = x2, y2
        elif image_dir == Direction.WEST:
            img_x1, img_y1 = x1, y1
            img_x2, img_y2 = x1 + (0.2 * (x2 - x1)), y2  # 20% width on the left

        # Draw the updated small image in the new position
        new_img_id = self.canvas.create_rectangle(
            img_x1, img_y1, img_x2, img_y2, fill="#C71585", tags="obstacle_image"
        )
        self.obstacle_dict[key]["img_id"] = new_img_id

    def toggle_obstacle(self, event):
        """Add or remove obstacles on the grid when clicked."""
        x = event.x // self.cell_size
        y = (self.grid_size - event.y) // self.cell_size
        key = (x, y)

        if key in self.obstacle_dict:
            self.canvas.delete(self.obstacle_dict[key]["rect_id"])
            self.canvas.delete(self.obstacle_dict[key]["img_id"])
            # Remove specific dropdown menu and label associated with this obstacle
            self.obstacle_dict[key]["label"].destroy()
            self.obstacle_dict[key]["menu"].destroy()
            del self.obstacle_dict[key]
        else:
            rect_id, img_id = self.draw_obstacle(x, y, Direction.NORTH)
            self.obstacle_dict[key] = {
                "rect_id": rect_id,
                "img_id": img_id,
                "img_dir": Direction.NORTH,
            }

            # Create dropdown to select image direction
            label = tk.Label(self.control_frame, text=f"Obstacle at ({x}, {y})")
            label.pack()

            direction_var = tk.StringVar(
                value=self.dir_enum_to_label[self.obstacle_dict[key]["img_dir"]]
            )
            direction_menu = tk.OptionMenu(
                self.control_frame,
                direction_var,
                "North",
                "South",
                "East",
                "West",
                command=lambda _: self.update_obstacle_image(
                    key, self.obstacle_dict[key]["img_id"], direction_var
                ),
            )
            direction_menu.pack()

            # Store the label and menu in the obstacle_dict so we can delete them later
            self.obstacle_dict[key]["label"] = label
            self.obstacle_dict[key]["menu"] = direction_menu

    def draw_obstacle(self, botleft_x, botleft_y, image_direction):
        """Draw obstacle at specified position with the given direction."""
        x1, y1 = botleft_x * self.cell_size, self.grid_size - (botleft_y + OBS_DIM) * self.cell_size
        x2, y2 = (botleft_x + OBS_DIM) * self.cell_size, self.grid_size - botleft_y * self.cell_size

        # Create the main obstacle rectangle and tag it
        rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="obstacle")

        # Create small image to represent the direction and tag it as well
        img_x1, img_y1, img_x2, img_y2 = 0, 0, 0, 0
        if image_direction == Direction.NORTH:
            img_x1, img_y1 = x1, y1
            img_x2, img_y2 = x2, y1 + (0.2 * (y2 - y1))
        elif image_direction == Direction.SOUTH:
            img_x1, img_y1 = x1, y2 - (0.2 * (y2 - y1))
            img_x2, img_y2 = x2, y2
        elif image_direction == Direction.EAST:
            img_x1, img_y1 = x2 - (0.2 * (x2 - x1)), y1
            img_x2, img_y2 = x2, y2
        elif image_direction == Direction.WEST:
            img_x1, img_y1 = x1, y1
            img_x2, img_y2 = x1 + (0.2 * (x2 - x1)), y2

        # Create small rectangle representing the image and tag it
        img_id = self.canvas.create_rectangle(img_x1, img_y1, img_x2, img_y2, fill="#C71585", tags="obstacle_image")
        
        return rect_id, img_id

    def run_algo(self):
        """Run the algorithm and move the car along the computed path."""
        print("Init MazeSolver object...")
        maze_solver = MazeSolver(WIDTH, HEIGHT, ROBOT_X, ROBOT_Y, Direction.NORTH)

        if not self.obstacle_dict:
            print("No Obstacles Initialized!")
            return

        # Parse obstacles and set them in the maze solver
        id_no = 1
        obstacles_json = []
        for key, value in self.obstacle_dict.items():
            obs_x, obs_y = key
            img_dir = value["img_dir"]
            obstacles_json.append({"x": obs_x, "y": obs_y, "id": id_no, "d": img_dir})
            maze_solver.add_obstacle(obs_x, obs_y, img_dir, id_no)
            id_no += 1

        # Get the optimal path from the algorithm
        print("Running algorithm...")
        start = time.time()
        optimal_path, distance = maze_solver.get_optimal_order_dp(retrying=False)
        print(f"Time taken to find shortest path using A* search: {time.time() - start}s")
        print(f"Distance to travel: {distance} units")
        print(f"Optimal path: {optimal_path}")
        # Based on the shortest path, generate commands for the robot
        commands = command_generator(optimal_path, obstacles_json)
        print(f"Commands: {commands}")

        # Move the car along the optimal path
        for step in optimal_path:
            x = step.x
            y = step.y
            direction = step.direction
            self.update_car_position(x, y, direction)

            # Simulate camera action randomly for demonstration
            if step.screenshot_id != -1:
                self.simulate_camera_action(direction)

            self.root.update()
            time.sleep(0.5)  # Simulate time delay between movements

# Create the Car Simulator and run the GUI
simulator = CarSimulator()
simulator.root.mainloop()
