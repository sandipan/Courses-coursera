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
        self.next_cell_x = 15  # Predefined position for the next cell to collapse.
        self.next_cell_y = 7  # Predefined position for the next cell to collapse.
    
        # Initialize a list of tile types available in the environment.
        self.tiles = [
            Tile({'top': 'B', 'bottom': 'B', 'left': 'A', 'right': 'A'}),
            Tile({'top': 'A', 'bottom': 'A', 'left': 'B', 'right': 'A'}), 
            Tile({'top': 'A', 'bottom': 'A', 'left': 'B', 'right': 'B'}), 
            Tile({'top': 'A', 'bottom': 'B', 'left': 'A', 'right': 'B'})
            # Additional tiles with different edge configurations can be added here.
        ]
    
        self.init_cells()  # Populate the grid with cells.

    def run(self):
        # Main update loop for managing the wave function collapse algorithm and displaying the grid.
        self.wave_function_collapse()
        self.display_grid()

    def wave_function_collapse(self):
        # Perform the wave function collapse by selecting the next cell to collapse based on predefined criteria.
        cell_x = self.next_cell_x
        cell_y = self.next_cell_y
            
        # Exit the function if no cell is selected.
        if cell_x is None or cell_y is None:
            return None
            
        # Collapse the selected cell to a single tile option.
        self.collapse_cell(cell_x, cell_y)
        
    def collapse_cell(self, x, y):
        # Collapse the specified cell to one of its possible tiles randomly.
        possibilities = self.cells[x][y]
        chosen_tile = random.choice(possibilities)  # Randomly select one of the possible tiles.
        self.cells[x][y] = [chosen_tile]  # Update the cell to only contain the chosen tile.
        
        # Propagate the collapse to adjacent cells
        self.propagate(x, y)
        
    def propagate(self, x, y):
        # Begin propagation from a collapsed cell to its neighbors to ensure consistency.
        collapsed_tile = self.cells[x][y][0]  # Retrieve the collapsed tile at the given coordinates.

        # Define the coordinates of direct neighbors (top, bottom, left, right).
        neighbors = {
            'top': (x, y - 1),
            'bottom': (x, y + 1),
            'left': (x - 1, y),
            'right': (x + 1, y)
        }

        # Iterate through each neighbor to potentially update its list of possible tiles.
        for direction, (nx, ny) in neighbors.items():
            # Check if neighbor coordinates are within the grid bounds.
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                # Update the neighbor based on the collapsed tile and direction.
                self.update_neighbors(nx, ny, collapsed_tile, direction)

    def update_neighbors(self, nx, ny, collapsed_tile, direction):
        # Retrieve the list of possible tiles for the neighbor cell.
        neighbor_possibilities = self.cells[nx][ny]

        # Proceed only if the neighbor cell has not already collapsed to a single tile.
        if len(neighbor_possibilities) > 1:
            # Iterate through a copy of the neighbor's possible tiles.
            for tile in neighbor_possibilities[:]:
                # Remove the tile from the original list if it's incompatible with the collapsed tile.
                if not tile.is_compatible(collapsed_tile, direction):
                    neighbor_possibilities.remove(tile)

          
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
                # Display the tile differently based on whether the cell has collapsed to a single option.
                if len(self.cells[x][y]) == 1:
                    tile = self.cells[x][y][0]
                    tile.display(x * tile_size, y * tile_size, tile_size, len(self.cells[x][y]))
                else:
                    tile = random.choice(self.cells[x][y])
                    tile.display_entropy(x * tile_size, y * tile_size, tile_size, len(self.cells[x][y]))
                    
                
            
        
        

        
    
