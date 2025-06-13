import random  # Import the random module.

class Tile:
    
    def __init__ (self, pos, cell_size, type):
        # Initialize a Tile with position, size, and type.
        self.pos = pos  # The position of the tile.
        self.cell_size = cell_size  # The size of the tile.
        # Tuple storing possible tile types.
        self.types = ("floor", "wall", "resource", "water")
        self.current_type = type  # The current type of the tile.
        self.isObstable = False  # Boolean flag for obstacle status.
        
    def run(self):
        # Call the display function to render the tile.
        self.display()
        
    def display(self):
        # Set the stroke color for drawing outlines.
        stroke(0,50)
        
        # Fill and draw a rectangle for the "floor" type.
        if(self.types[self.current_type] == "floor"):
            fill(255)  # White color for "floor".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        # Fill and draw a rectangle for the "wall" type.
        elif(self.types[self.current_type] == "wall"):
            fill(0)  # Black color for "wall".
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
        # Fill and draw a rectangle, then an ellipse for the "resource" type.
        elif(self.types[self.current_type] == "resource"):
            fill(255)  # White color for the background.
            rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
            ellipseMode(CORNER)  # Set ellipse mode to corner.
            fill(0,150,0)  # Green color for the "resource".
            ellipse(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
