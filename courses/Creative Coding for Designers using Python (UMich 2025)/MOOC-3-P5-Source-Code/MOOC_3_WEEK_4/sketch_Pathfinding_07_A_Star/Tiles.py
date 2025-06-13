import random  # Import the random module for potential use in generating random values or decisions.

class Tile:
    # Initialize a Tile object with its position, size, type, and grid information.
    def __init__(self, pos, cell_size, type, cols, rows, x, y, all_cells):
        self.pos = pos  # The position of the tile on the canvas.
        self.cell_size = cell_size  # The size of the tile.
        # Define possible types of tiles, including floor, wall, resource, water, and stockpile.
        self.types = ("floor", "wall", "resource", "water", "stokpile")
        self.current_type = type  # The current type of this tile.
        self.isObstable = False  # Flag to indicate if the tile is an obstacle.
        self.x = x  # The x-coordinate in the grid.
        self.y = y  # The y-coordinate in the grid.
        self.all_cells = all_cells  # Reference to all cells in the grid for neighbor lookup.
        self.cols = cols  # Total columns in the grid.
        self.rows = rows  # Total rows in the grid.
        self.visited = False  # Flag for whether the tile has been visited in search algorithms.
        self.parent = None  # Reference to the parent tile in pathfinding algorithms.
        self.g = 0  # Cost from the start node to this node.
        self.h = 0  # Heuristic estimate of cost from this node to the end node.
        self.f = 0  # Total cost (g + h), used to prioritize nodes in pathfinding.
        
        f = createFont("Consolas-Bold-14", 14)  # Create a font for potential text display.
        textFont(f)  # Set the created font as the current font for text rendering.
        
    def run(self):
        # Update and display the tile.
        self.display()
        
    def display(self):
        # Visual representation of the tile based on its type.
        stroke(0, 50)  # Set stroke color for tile borders.
        
        # Fill and draw the tile according to its type.
        if(self.types[self.current_type] == "floor"):
            fill(255)  # White for "floor".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        elif(self.types[self.current_type] == "wall"):
            fill(0)  # Black for "wall".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        elif(self.types[self.current_type] == "resource"):
            fill(255)  # Background for "resource".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
            ellipseMode(CORNER)  # Set ellipse mode for drawing.
            fill(0, 150, 0)  # Green for the resource icon.
            ellipse(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
    
    def display_highlight(self, col):
        # Highlight the tile with a given color.
        fill(col)  # Set the fill color for highlighting.
        stroke(0, 50)  # Set stroke color for highlighted tile borders.
        rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)  # Draw the highlighted rectangle.
    
    def change_type(self, type):
        # Change the tile's type and update its obstacle status accordingly.
        self.current_type = type  # Set the current type to the specified type.
        self.isObstable = True if type == 1 or type == 3 else False  # Set as an obstacle based on type.
    
    def get_neighbors(self):
        # Retrieve neighboring tiles based on the tile's position in the grid.
        neighbors = []
        # Add neighbors to the list based on their relative position.
        if self.x > 0: neighbors.append(self.all_cells[self.x - 1][self.y])  # Left neighbor.
        if self.x < self.cols - 1: neighbors.append(self.all_cells[self.x + 1][self.y])  # Right neighbor.
        if self.y > 0: neighbors.append(self.all_cells[self.x][self.y - 1])  # Top neighbor.
        if self.y < self.rows - 1: neighbors.append(self.all_cells[self.x][self.y + 1])  # Bottom neighbor.
        return neighbors  # Return the list of neighboring tiles.
