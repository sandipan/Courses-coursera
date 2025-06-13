import random  # Import random module for potential use in generating random values or decisions.

class Tile:
    # Initialize a Tile object with its attributes including position, size, and grid context.
    def __init__(self, pos, cell_size, type, cols, rows, x, y, all_cells):
        self.pos = pos  # Position of the tile on the canvas.
        self.cell_size = cell_size  # Size of the tile.
        self.types = ("floor", "wall", "resource", "water", "stockpile")  # Possible types a tile can be.
        self.current_type = type  # Current type of the tile.
        self.isObstable = False  # Indicates if the tile is an obstacle.
        self.x = x  # X-coordinate in the grid.
        self.y = y  # Y-coordinate in the grid.
        self.all_cells = all_cells  # Reference to all cells in the grid.
        self.cols = cols  # Number of columns in the grid.
        self.rows = rows  # Number of rows in the grid.
        self.visited = False  # Indicates if the tile has been visited in search algorithms.
        self.parent = None  # Parent tile in pathfinding algorithms.
        self.g = 0  # Cost from the start node to this node.
        self.h = 0  # Heuristic estimate of cost to reach the end node from this node.
        self.f = 0  # Total estimated cost (g + h) through the current node.
        
        # Set up for displaying cost values on the tile.
        f = createFont("Consolas-Bold-14", 14)  # Create a font for displaying text.
        textFont(f)  # Apply the created font for text rendering.
        
    def run(self):
        # Update and display the tile.
        self.display()
        self.display_data()  # Display pathfinding cost data on the tile.
    
    def display_data(self):
        # Display pathfinding data (g, h, and f costs) on the tile.
        fill(0)  # Set text color to black for visibility.
        
        # Display the cost from the start node to this node (g).
        my_text = "g:" + str(self.g)
        text(my_text, self.pos.x + 2, self.pos.y + self.cell_size - 2)
        
        # Display the heuristic estimate to reach the end node (h).
        my_text = "h:" + str(int(self.h))
        text(my_text, self.pos.x + 2, self.pos.y + self.cell_size - 16)
        
        # Display the total estimated cost (f = g + h).
        my_text = "f:" + str(int(self.f))
        text(my_text, self.pos.x + 2, self.pos.y + self.cell_size - 32)
    
    def display(self):
        # Visual representation of the tile based on its current type.
        stroke(0, 50)  # Set stroke color for tile borders.
        
        # Fill and draw the tile according to its type.
        if self.types[self.current_type] == "floor":
            fill(255)  # White for "floor".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        elif self.types[self.current_type] == "wall":
            fill(0)  # Black for "wall".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        elif self.types[self.current_type] == "resource":
            fill(255)  # Background color for "resource".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
            fill(0, 150, 0)  # Green for resource symbol.
            ellipse(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
    
    def display_highlight(self, col):
        # Highlight the tile with a specified color.
        fill(col)  # Set the fill color for highlighting.
        stroke(0, 50)  # Set stroke color for highlighted tile borders.
        rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)  # Draw highlighted rectangle.
    
    def change_type(self, type):
        # Change the tile's type and update its obstacle status accordingly.
        self.current_type = type
        self.isObstable = True if type == 1 or type == 3 else False  # Set as obstacle based on type.
    
             
    def get_neighbors(self):
        # Retrieve neighboring tiles based on the tile's grid position.
        neighbors = []  # Initialize an empty list to hold neighbor tiles.
        # Check and append the left neighbor if it exists.
        if self.x > 0: 
            neighbors.append(self.all_cells[self.x - 1][self.y])
        # Check and append the right neighbor if it exists.
        if self.x < self.cols - 1: 
            neighbors.append(self.all_cells[self.x + 1][self.y])
        # Check and append the top neighbor if it exists.
        if self.y > 0: 
            neighbors.append(self.all_cells[self.x][self.y - 1])
        # Check and append the bottom neighbor if it exists.
        if self.y < self.rows - 1: 
            neighbors.append(self.all_cells[self.x][self.y + 1])
        return neighbors  # Return the list of neighboring tiles.

        
        
