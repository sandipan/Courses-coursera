import random  # Import random module for selecting random tiles.
from Tiles import Tile  # Import the Tile class to create and manage tile objects.

class Environment:
    # Initialize the environment with its dimensions and create a grid of cells.
    def __init__(self, cols, rows, world_x, world_y):
        self.cols = cols  # Number of columns in the grid.
        self.rows = rows  # Number of rows in the grid.
        self.world_x = world_x  # Physical width of the environment.
        self.world_y = world_y  # Physical height of the environment.
        self.cells = []  # Grid to store cells.
    
        # Initialize a list of tile types available in the environment.
        self.tiles = [
            Tile({'top': 'B', 'bottom': 'B', 'left': 'A', 'right': 'A'}),
            # Additional tiles with different edge configurations can be added here.
        ]
    
        self.init_cells()  # Populate the grid with cells.

    def run(self):
        # Update function called typically in a loop to display the grid.
        self.display_grid()

    def init_cells(self):
        # Initialize each cell in the grid with a list of all possible tiles.
        for i in range(self.cols):
            row = []
            for j in range(self.rows):
                # Use slice notation to create a copy of the tiles list for each cell.
                row.append(self.tiles[:])
            self.cells.append(row)

    def display_grid(self):
        # Display the grid with tiles based on their current state.
        tile_size = float(self.world_x) / self.cols  # Calculate the size of each tile.
        for x in range(self.cols):
            for y in range(self.rows):
                # If a cell has collapsed to a single tile option, display it normally.
                if len(self.cells[x][y]) == 1:
                    tile = self.cells[x][y][0]
                    tile.display(x * tile_size, y * tile_size, tile_size, len(self.cells[x][y]))
                # If a cell has multiple possible tiles, display one randomly with entropy.
                else:
                    tile = random.choice(self.cells[x][y])
                    tile.display_entropy(x * tile_size, y * tile_size, tile_size, len(self.cells[x][y]))
