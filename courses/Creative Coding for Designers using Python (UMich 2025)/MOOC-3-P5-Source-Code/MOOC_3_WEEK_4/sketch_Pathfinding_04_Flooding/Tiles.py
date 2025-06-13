import random  # Import the random module.

class Tile:
    
    def __init__(self, pos, cell_size, type, cols, rows, x, y, all_cells):
        # Initialize the Tile object with its position, size, type, and grid information.
        self.pos = pos  # The position of the tile.
        self.cell_size = cell_size  # The size of the tile.
        self.types = ("floor", "wall", "resource", "water", "stokpile")  # Possible types of tiles.
        self.current_type = type  # The current type of this tile.
        self.isObstable = False  # Indicates if the tile is an obstacle.
        self.x = x  # The x-coordinate in the grid.
        self.y = y  # The y-coordinate in the grid.
        self.all_cells = all_cells  # Reference to all cells in the grid.
        self.cols = cols  # Total columns in the grid.
        self.rows = rows  # Total rows in the grid.
        self.visited = False  # Indicates if the tile has been visited (for algorithms).
        
    def run(self):
        # Call the display function to render the tile.
        self.display()
        
    def display(self):
        # Set the stroke and draw the tile based on its type.
        stroke(0, 50)  # Stroke color with some transparency.
        
        # Colors for unvisited and visited states (not used in this method).
        non_visit_color = color(255)  # White for non-visited.
        visited_color = color(0, 0, 255)  # Blue for visited.
        
        # Drawing logic based on the tile's type.
        if self.types[self.current_type] == "floor":
            fill(255)  # White color for "floor".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        elif self.types[self.current_type] == "wall":
            fill(0)  # Black color for "wall".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        elif self.types[self.current_type] == "resource":
            fill(255)  # Background color for "resource".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
            ellipseMode(CORNER)  # Set ellipse drawing mode.
            fill(0, 150, 0)  # Green color for the resource ellipse.
            ellipse(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
    
    def display_highlight(self, col):
        # Highlight the tile with a specific color.
        fill(col)  # Set the fill color to the specified color.
        rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        
    def get_neighbors(self):
        # Get the neighboring tiles of the current tile.
        neighbors = []
        # Add neighbor to the left.
        if self.x > 0: neighbors.append(self.all_cells[self.x - 1][self.y])
        # Add neighbor to the right.
        if self.x < self.cols - 1: neighbors.append(self.all_cells[self.x + 1][self.y])
        # Add neighbor above.
        if self.y > 0: neighbors.append(self.all_cells[self.x][self.y - 1])
        # Add neighbor below.
        if self.y < self.rows - 1: neighbors.append(self.all_cells[self.x][self.y + 1])
        return neighbors  # Return the list of neighboring tiles.
