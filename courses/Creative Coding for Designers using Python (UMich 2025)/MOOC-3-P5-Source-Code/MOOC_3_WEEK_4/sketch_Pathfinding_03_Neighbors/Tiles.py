import random  # Import the random module.

class Tile:
    
    def __init__ (self, pos, cell_size, type, cols, rows, x, y, all_cells):
        # Initialize a Tile with various attributes including position, size, and type.
        self.pos = pos  # The position of the tile on the canvas.
        self.cell_size = cell_size  # The size of the tile.
        # Define the possible types of tiles.
        self.types = ("floor", "wall", "resource", "water", "stokpile")
        self.current_type = type  # The current type of the tile.
        self.isObstable = False  # Flag to indicate if the tile is an obstacle.
        self.x = x  # The x-coordinate of the tile in the grid.
        self.y = y  # The y-coordinate of the tile in the grid.
        self.all_cells = all_cells  # Reference to the grid of all cells/tiles.
        self.cols = cols  # Number of columns in the grid.
        self.rows = rows  # Number of rows in the grid.
        
    def run(self):
        # Call the display function to render the tile.
        self.display()
        
    def display(self):
        # Set the stroke color and draw the tile based on its type.
        stroke(0, 50)  # Stroke color set with a transparency.
        
        # Drawing logic based on the tile's type.
        if(self.types[self.current_type] == "floor"):
            fill(255)  # Set fill color for "floor" type.
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        elif(self.types[self.current_type] == "wall"):
            fill(0)  # Set fill color for "wall" type.
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        elif(self.types[self.current_type] == "resource"):
            fill(255)  # Background fill for "resource".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
            ellipseMode(CORNER)  # Set mode for drawing ellipses.
            fill(0, 150, 0)  # Set fill color for the ellipse.
            ellipse(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
    
    def display_highlight(self, col):
        # Highlight the tile with a given color.
        fill(col)  # Set the fill color.
        rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        
    def get_neighbors(self):
        # Get neighboring tiles based on the tile's position.
        neighbors = []  # Initialize an empty list for neighbors.
        # Append neighbors to the list based on conditional checks.
        if self.x > 0: neighbors.append(self.all_cells[self.x - 1][self.y])
        if self.x < self.cols - 1: neighbors.append(self.all_cells[self.x + 1][self.y])
        if self.y > 0: neighbors.append(self.all_cells[self.x][self.y - 1])
        if self.y < self.rows - 1: neighbors.append(self.all_cells[self.x][self.y + 1])
        return neighbors  # Return the list of neighbors.
