import random  # Import the random module.
from Tiles import Tile  # Import the Tile class.

class Environment:
    
    def __init__(self, cols, rows, world_x, world_y):
        # Initialize the Environment with its dimensions.
        self.cols = cols  # Number of columns.
        self.rows = rows  # Number of rows.
        self.world_x = world_x  # World width.
        self.world_y = world_y  # World height.
        self.cells = []  # List to store cell instances.
        
        self.init_cells()  # Populate the cells list.
    
    def run(self):
        # Process/run operations for each tile.
        self.run_tiles()
        # Uncomment to print the number of cells.
        #println(len(self.cells))
        
    def run_tiles(self):
        # Execute the run method for each tile in cells.
        for t in self.cells:
            t.run()
                
    def init_cells(self):
        # Calculate cell size and initialize cells.
        cell_size = float(self.world_x) / self.cols  # Determine the size of each cell.
        println(cell_size)  # Print cell size (for debugging or information).
        for i in range(self.cols):  # Iterate through columns.
            for j in range(self.rows):  # Iterate through rows.
                pos = PVector(i*cell_size, j*cell_size)  # Calculate position for the tile.
                new_tile = Tile(pos, cell_size, 0)  # Create a new Tile instance.
                self.cells.append(new_tile)  # Add the new tile to the cells list.
    
    def paint_cell(self, index, type):
        # Change the type of a specific cell by its index.
        if index < len(self.cells):  # Check if index is within bounds.
            self.cells[index].current_type = type  # Update the cell's type.
        
    def get_cell(self, x, y):
        # Calculate the index of the cell based on x, y coordinates.
        x = int(x / (float(self.world_x) / self.cols))  # Convert x to column index.
        y = int(y / (float(self.world_y) / self.rows))  # Convert y to row index.
        
        index = (self.rows * x) + y  # Calculate linear index from 2D position.
        
        if 0 <= index < len(self.cells):  # Check if index is within bounds.
            return index  # Return the index of the cell.
        else:
            raise IndexError("Vector index out of range.")  # Index out of bounds.
