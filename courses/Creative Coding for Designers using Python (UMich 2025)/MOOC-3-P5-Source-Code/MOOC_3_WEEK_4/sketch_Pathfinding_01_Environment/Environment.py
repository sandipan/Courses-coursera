import random  # Import the random module.
from Tiles import Tile  # Import the Tile class from the Tiles module.

class Environment:
    
    def __init__(self, cols, rows, world_x, world_y):
        # Initialize the Environment with dimensions and world size.
        self.cols = cols  # Number of columns.
        self.rows = rows  # Number of rows.
        self.world_x = world_x  # Width of the world.
        self.world_y = world_y  # Height of the world.
        self.cells = []  # List to store cell objects.
        
        self.init_cells()  # Initialize the cells.
    
    def run(self):
        # Process each tile for the current frame.
        self.run_tiles()
        # Uncomment to print the number of cells.
        #println(len(self.cells))
        
    def run_tiles(self):
        # Iterate through each cell and execute its run method.
        for t in self.cells:
            t.run()
                
    def init_cells(self):
        # Calculate the size of each cell.
        cell_size = float(self.world_x) / self.cols
        # Uncomment to print the size of each cell.
        println(cell_size)
        # Generate tiles for each cell position.
        for i in range(self.cols):
            for j in range (self.rows):
                pos = PVector(i*cell_size, j * cell_size)  # Calculate position vector.
                new_tile = Tile(pos, cell_size, 0)  # Create a new tile.
                self.cells.append(new_tile)  # Add the new tile to the cells list.
