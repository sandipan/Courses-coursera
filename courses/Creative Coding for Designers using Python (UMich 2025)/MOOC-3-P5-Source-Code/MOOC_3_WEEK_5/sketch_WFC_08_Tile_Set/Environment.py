import random
from Tiles import Tile  # Import Tile class from Tiles module.

class Environment:
    
    def __init__(self, cols, rows, world_x, world_y):
        # Initialize Environment object with specified parameters.
        self.cols = cols  # Number of columns in the environment grid.
        self.rows = rows  # Number of rows in the environment grid.
        self.world_x = world_x  # Width of the world.
        self.world_y = world_y  # Height of the world.
        self.cells = []  # List to store cells in the grid.
        self.next_cell_x = 15  # Initial x-coordinate of the next cell to be processed.
        self.next_cell_y = 7   # Initial y-coordinate of the next cell to be processed.
        
        # Load images for different tile configurations.
        img_AAAA = loadImage("AAAA.jpg")
        img_AABA = loadImage("AABA.jpg")
        img_AABB = loadImage("AABB.jpg")
        img_ABAB = loadImage("ABAB.jpg")
        img_ABBA = loadImage("ABBA.jpg")
        img_BAAA = loadImage("BAAA.jpg")
        img_BAAB = loadImage("BAAB.jpg")
        img_BABA = loadImage("BABA.jpg")
        img_BABB = loadImage("BABB.jpg")
        img_BBAA = loadImage("BBAA.jpg")
        img_BBBA = loadImage("BBBA.jpg")
        img_BBBB = loadImage("BBBB.jpg")    
        img_AAAB = loadImage("AAAB.jpg")
        img_ABBB = loadImage("ABBB.jpg")
        img_BBAB = loadImage("BBAB.jpg")
        img_ABAA = loadImage("ABAA.jpg")
    
        # Define tiles with edges and corresponding images.
        self.tiles = [
            Tile({'top': 'A', 'bottom': 'A', 'left': 'A', 'right': 'A'}, img_AAAA),
            Tile({'top': 'A', 'bottom': 'A', 'left': 'B', 'right': 'A'}, img_AABA), 
            Tile({'top': 'A', 'bottom': 'A', 'left': 'B', 'right': 'B'}, img_AABB), 
            Tile({'top': 'A', 'bottom': 'B', 'left': 'A', 'right': 'B'}, img_ABAB), 
            Tile({'top': 'A', 'bottom': 'B', 'left': 'B', 'right': 'A'}, img_ABBA), 
            Tile({'top': 'B', 'bottom': 'A', 'left': 'A', 'right': 'A'}, img_BAAA),
            Tile({'top': 'B', 'bottom': 'A', 'left': 'A', 'right': 'B'}, img_BAAB),
            Tile({'top': 'B', 'bottom': 'A', 'left': 'B', 'right': 'A'}, img_BABA),
            Tile({'top': 'B', 'bottom': 'A', 'left': 'B', 'right': 'B'}, img_BABB),
            Tile({'top': 'B', 'bottom': 'B', 'left': 'A', 'right': 'A'}, img_BBAA),
            Tile({'top': 'B', 'bottom': 'B', 'left': 'B', 'right': 'A'}, img_BBBA),
            Tile({'top': 'B', 'bottom': 'B', 'left': 'B', 'right': 'B'}, img_BBBB),
            Tile({'top': 'A', 'bottom': 'A', 'left': 'A', 'right': 'B'}, img_AAAB),
            Tile({'top': 'A', 'bottom': 'B', 'left': 'A', 'right': 'A'}, img_ABAA),
            Tile({'top': 'A', 'bottom': 'B', 'left': 'B', 'right': 'B'}, img_ABBB),
            Tile({'top': 'B', 'bottom': 'B', 'left': 'A', 'right': 'B'}, img_BBAB) 
            # ... More tiles
        ]
    
        self.init_cells()  # Initialize the environment grid with tiles.
    
    def init_cells(self):
        # Initialize the environment grid with tiles.
        for i in range(self.cols):
            row = []
            for j in range (self.rows):
                row.append(self.tiles[:])  # Add a copy of the list of tiles to each cell.
            self.cells.append(row)


    def run(self):
        # Main update loop for managing the wave function collapse algorithm and displaying the grid.
        self.wave_function_collapse()  # Collapse cells according to the wave function collapse algorithm.
        self.display_grid()  # Display the grid.
        
        # Find the cell with the lowest entropy and display it.
        self.find_lowest_entropy_cell()  
        self.display_lowest_entropy(self.next_cell_x, self.next_cell_y)
        
        # If there's a cell with known coordinates, display its possibilities.
        if self.next_cell_x is not None and self.next_cell_y is not None:
            possibilities = self.cells[self.next_cell_x][self.next_cell_y]
            self.display_possibilities(possibilities, self.next_cell_x, self.next_cell_y)
        
    def wave_function_collapse(self):
        # Perform the wave function collapse by selecting the next cell to collapse based on predefined criteria.
        cell_x = self.next_cell_x
        cell_y = self.next_cell_y
            
        # Exit the function if no cell is selected.
        if cell_x is None or cell_y is None:
            return None
            
        # Collapse the selected cell to a single tile option.
        self.collapse_cell(cell_x, cell_y)
        
    def find_lowest_entropy_cell(self):
        # Identify the cell with the lowest entropy (number of tile options) for the next collapse.
        lowest_entropy = 1000000  # Start with a very high entropy value for comparison.
        cell_x, cell_y = None, None  # Initialize variables to store coordinates of the cell with lowest entropy.
        
        several_lowest = []  # List to store coordinates of all cells with the lowest entropy found.
        
        # Iterate through the grid to evaluate the entropy of each cell.
        for x in range(self.cols):
            for y in range(self.rows):
                entropy = len(self.cells[x][y])  # Entropy is defined as the number of possible tiles.
                # If a cell's entropy is lower than the current lowest (and the cell has more than one option), update the lowest entropy.
                if 1 < entropy < lowest_entropy:
                    several_lowest = []  # Reset the list of lowest entropy cells as a new lowest has been found.
                    lowest_entropy = entropy  # Update the lowest entropy value.
                    cell_x, cell_y = x, y  # Update the coordinates of the cell with the new lowest entropy.
                    several_lowest.append((x, y))  # Add the cell to the list of lowest entropy cells.
                elif entropy == lowest_entropy:
                    cell_x, cell_y = x, y  # Update the coordinates to the current cell (same lowest entropy found).
                    several_lowest.append((x, y))  # Add the cell to the list of lowest entropy cells.
        
        # If there are multiple cells with the same lowest entropy, randomly select one.
        if len(several_lowest) > 1:
            cell = random.choice(several_lowest)  # Choose randomly among the cells with the lowest entropy.
            self.next_cell_x = cell[0]  # Update the next cell to collapse with the chosen cell's x-coordinate.
            self.next_cell_y = cell[1]  # Update the next cell to collapse with the chosen cell's y-coordinate.
            return cell[0], cell[1]  # Return the coordinates of the chosen cell.
        else:
            self.next_cell_x = cell_x  # Set the next cell to collapse to the found lowest entropy cell.
            self.next_cell_y = cell_y
            return cell_x, cell_y  # Return the coordinates of the cell with the lowest entropy.
       
        
    def collapse_cell(self, x, y):
        possibilities = self.cells[x][y]
        
        # Randomly select one of the remaining possible tiles to collapse
        chosen_tile = random.choice(possibilities)
        self.cells[x][y] = [chosen_tile]
        
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
    
    def display_possibilities(self, possibilities, offset_x, offset_y):
        # Display the possible tiles for a cell visually in the interface.
        
        tile_size = float(self.world_x) / self.cols  # Calculate the size of each tile.
        offset_x = offset_x * tile_size + 60  # Adjust the x offset based on tile size and an arbitrary value for padding.
        offset_y = offset_y * tile_size - 60  # Adjust the y offset based on tile size and an arbitrary value for padding.
        
        stroke(255)  # Set the outline color for the background rectangle.
        fill(50)  # Set the fill color for the background rectangle.
        x_size = len(possibilities) * (tile_size + 10) + 10  # Calculate the width of the background rectangle based on the number of possibilities.
        rect(0 + offset_x, 0 + offset_y, x_size, 60)  # Draw the background rectangle.
        
        x_pos = 10 + offset_x  # Initialize the x position for the first tile.
        for p in possibilities:
            p.display_image(x_pos, 10 + offset_y, tile_size, 1) #display the image
            x_pos += tile_size + 10  # Update the x position for the next tile, adding some padding.
            
    def display_lowest_entropy(self, x, y):
        # Highlight the cell with the lowest entropy to indicate where the next collapse will occur.
        if x is not None and y is not None:  # Ensure the coordinates are valid.
            tile_size = float(self.world_x) / self.cols  # Calculate the size of each tile.
            
            stroke(255, 0, 0)  # Set the stroke color to red for visibility.
            noFill()  # Disable filling to only draw the outline.
            strokeWeight(3)  # Increase the stroke weight to make the highlight stand out.
            pushMatrix()  # Save the current drawing style settings and transformations.
            translate(x * tile_size, y * tile_size)  # Move the origin to the specified location.
            rectMode(CORNER)  # Set the rectangle drawing mode to CORNER.
            rect(0, 0, tile_size, tile_size)  # Draw a rectangle to highlight the cell.
            popMatrix()  # Restore the prior drawing style settings and transformations.
            strokeWeight(1)  # Reset the stroke weight back to the default.

    def display_grid(self):
        # Display the grid with tiles based on their current state.
        tile_size = float(self.world_x) / self.cols  # Calculate the size of each tile.
        for x in range(self.cols):
            for y in range(self.rows):
                # Display the tile differently based on whether the cell has collapsed to a single option.
                if len(self.cells[x][y]) == 1:
                    tile = self.cells[x][y][0]
                    tile.display_image(x * tile_size, y * tile_size, tile_size, len(self.cells[x][y]) ) #display the image
                else:
                    tile = random.choice(self.cells[x][y])
                    tile.display_entropy(x * tile_size, y * tile_size, tile_size, len(self.cells[x][y]))
                    
                
            
        
        

        
    
