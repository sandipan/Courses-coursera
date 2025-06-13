import random  # Import the random module for potential use.
from Tiles import Tile  # Import the Tile class from the Tiles module.

class Environment:
    
    def __init__(self, cols, rows, world_x, world_y):
        # Initialize environment with grid dimensions and world size.
        self.cols = cols  # Number of columns in the grid.
        self.rows = rows  # Number of rows in the grid.
        self.world_x = world_x  # Width of the environment in pixels.
        self.world_y = world_y  # Height of the environment in pixels.
        self.cells = []  # List to store cell (tile) objects.
        
        self.init_cells()  # Populate the grid with Tile objects.
        
        # Variables for managing the simulation state.
        self.running = False  # Flag to control the running state of the simulation.
        self.start_node = None  # Starting point for the flood fill.
        self.end_node = None  # Target point for the flood fill.
        self.stack = []  # Stack used for the flood fill algorithm.
        
        # Initialize start and end nodes and append start node to the stack.
        self.start_node = self.get_cell(100, 100)
        self.end_node = self.get_cell(1000, 400)
        self.stack.append(self.start_node)
        
    def run(self):
        # Execute each frame's logic: updating tiles, visualizing and executing flood fill.
        self.run_tiles()
        self.draw_visited()  # Highlight visited cells.
        self.draw_stack()  # Highlight cells in the stack.
        self.draw_start()  # Highlight the start node.
        self.draw_end()  # Highlight the end node.
        self.flood_fill()  # Perform the flood fill algorithm.
    
    def draw_start(self):
        # Highlight the start node with red color.
        col = color(255, 0, 0)
        self.start_node.display_highlight(col)
    
    def draw_end(self):
        # Highlight the end node with green color.
        col = color(0, 255, 0)
        self.end_node.display_highlight(col)
    
    def draw_stack(self):
        # Highlight all cells in the stack with cyan color.
        col = color(0, 255, 255)
        for cell in self.stack:
            cell.display_highlight(col)
            
    def draw_visited(self):
        # Highlight all visited cells with blue color.
        col = color(0, 0, 255)
        for column in self.cells:
            for cell in column:
                if cell.visited:
                    cell.display_highlight(col)
      
    def flood_fill(self):
        # Perform flood fill algorithm if running is True.
        if self.running:        
            if len(self.stack) > 0:
                # Pop the first cell from the stack, mark it visited.
                current_cell = self.stack.pop(0)
                current_cell.visited = True
                
                # Check if the current cell is the end node.
                if current_cell == self.end_node:
                    println("Goal Reached!")
                    self.running = False  # Stop the algorithm.
            
                # For each unvisited neighbor, mark it visited and add to the stack.
                for neighbor in current_cell.get_neighbors():
                    if not neighbor.visited:
                        neighbor.visited = True
                        self.stack.append(neighbor)
    
    def draw_neighbors(self, x, y):
        # Highlight a cell and its neighbors for visual inspection.
        cell = self.get_cell(x, y)
        col = color(255, 0, 0)  # Red for selected cell.
        cell.display_highlight(col)
        
        # Highlight neighbors in blue.
        neighbors = cell.get_neighbors()
        for n in neighbors:
            col = color(0, 0, 255)
            n.display_highlight(col)
    
    def run_tiles(self):
        # Call the run method on each Tile object in the grid.
        for column in self.cells:
            for cell in column:
                cell.run()
                
    def init_cells(self):
        # Initialize cells based on the environment size and grid dimensions.
        cell_size = float(self.world_x) / self.cols  # Calculate cell size.
        for i in range(self.cols):
            self.cells.append([])  # Add a new column.
            for j in range(self.rows):
                # Create and add new tiles to the column.
                pos = PVector(i * cell_size, j * cell_size)
                new_tile = Tile(pos, cell_size, 0, self.cols, self.rows, i, j, self.cells)
                self.cells[i].append(new_tile)
    
    
    def paint_cell(self, x, y, type):
        # Change the type of a cell based on given x, y coordinates and type.
        cell = self.get_cell(x, y)  # Retrieve the cell at specified coordinates.
        if(cell is not None):  # If the cell exists...
            cell.current_type = type  # Set the cell's type to the specified type.
      
    def get_cell(self, x, y):
        # Convert x, y screen coordinates to grid coordinates and retrieve the corresponding cell.
        x = int(x / (float(self.world_x) / self.cols))  # Calculate column index.
        y = int(y / (float(self.world_y) / self.rows))  # Calculate row index.
        
        # Check if the calculated indices are within the bounds of the cell grid.
        if (x < len(self.cells) and y < len(self.cells[0])):
            cell = self.cells[x][y]  # Retrieve the cell at the calculated indices.
            return cell  # Return the retrieved cell.
        else:
            return None  # Return None if the indices are out of bounds.

    
       
            
        
        

        
    
