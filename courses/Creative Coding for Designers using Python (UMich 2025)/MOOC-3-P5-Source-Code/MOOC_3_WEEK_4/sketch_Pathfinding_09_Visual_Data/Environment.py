import random  # Import random module for potential use in generating random values.
from Tiles import Tile  # Import the Tile class to represent each cell in the environment.

class Environment:
    # Initialize the environment with grid dimensions and physical size.
    def __init__(self, cols, rows, world_x, world_y):
        self.cols = cols  # Number of columns in the grid.
        self.rows = rows  # Number of rows in the grid.
        self.world_x = world_x  # Physical width of the environment.
        self.world_y = world_y  # Physical height of the environment.
        self.cells = []  # List to store the grid's cells.
        
        self.init_cells()  # Initialize and populate the grid with cells.
        
        # Variables to manage the state of the environment and pathfinding.
        self.running = False  # Controls if the pathfinding is active.
        self.path_found = False  # Indicates if a path has been found.
        self.start_node = None  # Starting cell for pathfinding.
        self.end_node = None  # Target cell for pathfinding.
        self.stack = []  # Open list for A* search.
        self.closed_stack = []  # Closed list for A* search.
        self.path = []  # List to store the final path.
        
        # Initialize the start and end nodes and add start node to the stack.
        self.start_node = self.get_cell(100, 100)
        self.end_node = self.get_cell(1000, 400)
        self.stack.append(self.start_node)
        
     # Main loop to update the environment.
    def run(self):
        self.run_tiles()  # Update each cell.
        self.draw_visited()  # Highlight visited cells.
        self.draw_stack()  # Highlight cells in the open list.
        self.draw_path()  # Highlight the final path if found.
        self.draw_start()  # Highlight the start cell.
        self.draw_end()  # Highlight the end cell.
        self.a_star_search()  # Execute A* search if running.
        #self.draw_data()  # Call draw_data to display pathfinding data on each cell.
        self.draw_visual_data()  # Call draw_visual_data to visually represent data on each cell in the stack.

    def draw_visual_data(self):
        # Iterate through all cells in the stack and visually display their data.
        for cell in self.stack:  # For each cell currently in the stack...
            cell.display_visual_data()  # Call the cell's method to display its visual data representation.

                
    def draw_data(self):
        # Iterate through all cells in the grid to display their pathfinding data.
        for column in self.cells:  # For each column in the grid...
            for cell in column:  # For each cell in the column...
                cell.display_data()  # Call the cell's method to display its pathfinding data.

    # Helper functions for visualizing various states of the environment.
    def draw_start(self):
        col = color(255,0,0)  # Red color for start node.
        self.start_node.display_highlight(col)
    
    def draw_end(self):
        col = color(0,255,0)  # Green color for end node.
        self.end_node.display_highlight(col)
    
    def draw_stack(self):
        col = color(0,255,255)  # Cyan color for stack nodes.
        for cell in self.stack:
            cell.display_highlight(col)
            
    def draw_visited(self):
        col = color(0,0,255)  # Blue color for visited nodes.
        for column in self.cells:
            for cell in column:
                if cell.visited:
                    cell.display_highlight(col)
                    
    def draw_path(self):
        if self.path_found:
            col = color(255,0,255)  # Magenta color for the path.
            for cell in self.path:
                cell.display_highlight(col)
                
    # Implementation of the A* search algorithm.
    def a_star_search(self):
        if self.running and len(self.stack) > 0:
            current_cell = self.find_closest_f(self.stack)  # Find cell in open list with lowest F cost.
            
            # Check if current cell is the end node.
            if current_cell == self.end_node:
                println("Goal Reached!")  # Announce goal reached.
                self.running = False
                self.path_found = True
                self.reconstruct_path(current_cell)  # Reconstruct the path from end to start.
                
            # Move current cell from open to closed list.
            self.stack.remove(current_cell)
            self.closed_stack.append(current_cell)
            
            # Process each neighbor of the current cell.
            for neighbor in current_cell.get_neighbors():
                if neighbor in self.closed_stack or neighbor.isObstable:
                    continue  # Skip already processed or obstacle cells.
                tentative_g = current_cell.g + 1  # Tentative G cost to the neighbor.
                new_path = False  # Flag to indicate if a better path is found.
                if neighbor not in self.stack or tentative_g < neighbor.g:
                    neighbor.g = tentative_g  # Update G cost.
                    new_path = True
                    if neighbor not in self.stack:
                        self.stack.append(neighbor)  # Add unvisited neighbor to open list.
                if new_path:
                    neighbor.h = dist(neighbor.pos.x, neighbor.pos.y, self.end_node.pos.x, self.end_node.pos.y)  # Calculate H cost.
                    neighbor.f = neighbor.g + neighbor.h  # Update F cost.
                    neighbor.parent = current_cell  # Set current cell as parent for path reconstruction.
        else:
            println("No solution!")  # Announce if no solution is found.
            self.running = False
            
    # Utility function to find the cell with the lowest F cost in the open list.
    def find_closest_f(self, my_list):
        lowest_f = 100000  # Arbitrary large number for comparison.
        lowest_f_node = None
        for node in my_list:
            if node.f < lowest_f:
                lowest_f = node.f
                lowest_f_node = node
        return lowest_f_node
    
    def flood_fill(self):
        # Execute the flood fill algorithm if the simulation is active.
        if self.running and len(self.stack) > 0:
            current_cell = self.stack.pop(0)  # Remove and use the first cell in the stack.
            current_cell.visited = True  # Mark the current cell as visited.
            
            # Check if the current cell is the end node to conclude the search.
            if current_cell == self.end_node:
                println("Goal Reached!")  # Indicate that the goal has been reached.
                self.running = False  # Stop the algorithm.
                self.path_found = True  # Indicate that a path has been found.
                self.reconstruct_path(current_cell)  # Reconstruct the path from end to start.
            
            # Process each unvisited and accessible neighbor of the current cell.
            for neighbor in current_cell.get_neighbors():
                if not neighbor.visited and not neighbor.isObstable:
                    neighbor.visited = True  # Mark the neighbor as visited.
                    self.stack.append(neighbor)  # Add the neighbor to the stack for further exploration.
                    neighbor.parent = current_cell  # Set the current cell as the parent for path reconstruction.
                        
    def reconstruct_path(self, current_cell):
        # Reconstruct the path from the end node to the start node using parent references.
        while current_cell.parent is not None:
            self.path.append(current_cell)  # Add the current cell to the path.
            current_cell = current_cell.parent  # Move to the parent cell.
        self.path.append(self.start_node)  # Ensure the start node is included in the path.
        println("Reconstruction Ended")  # Indicate that path reconstruction has finished.
            
    def draw_neighbors(self, x, y):
        # Highlight a cell and its neighbors for visual inspection.
        cell = self.get_cell(x, y)  # Retrieve the specified cell.
        col = color(255, 0, 0)  # Use red to highlight the selected cell.
        cell.display_highlight(col)  # Highlight the selected cell.
        
        # Highlight each neighbor of the selected cell in blue.
        neighbors = cell.get_neighbors()
        for n in neighbors:
            col = color(0, 0, 255)  # Use blue for neighbors.
            n.display_highlight(col)  # Highlight the neighbor.
    
    def run_tiles(self):
        # Update and draw each cell in the grid.
        for column in self.cells:
            for cell in column:
                cell.run()  # Execute each cell's run method.
                
    def init_cells(self):
        # Initialize the grid with Tile objects based on the environment size.
        cell_size = float(self.world_x) / self.cols  # Calculate the size of each cell.
        for i in range(self.cols):
            self.cells.append([])  # Prepare a list for each column.
            for j in range(self.rows):
                pos = PVector(i * cell_size, j * cell_size)  # Determine the position of each cell.
                # Create a new Tile object and add it to the appropriate column.
                new_tile = Tile(pos, cell_size, 0, self.cols, self.rows, i, j, self.cells)
                self.cells[i].append(new_tile)
    
    def paint_cell(self, x, y, type):
        # Change the type of a cell based on its coordinates.
        cell = self.get_cell(x, y)  # Retrieve the cell at the specified coordinates.
        if(cell is not None):
            cell.change_type(type)  # Use the cell's method to change its type.
    
    def get_cell(self, x, y):
        # Convert screen coordinates to grid coordinates and retrieve the corresponding cell.
        x = int(x / (float(self.world_x) / self.cols))  # Calculate the column index.
        y = int(y / (float(self.world_y) / self.rows))  # Calculate the row index.
        
        # Check if the calculated indices are within the grid bounds and return the cell if so.
        if (x < len(self.cells) and y < len(self.cells[0])):
            return self.cells[x][y]  # Return the cell at the calculated indices.
        else:
            return None  # Return None if the indices are out of bounds.
    
       
            
        
        

        
    
