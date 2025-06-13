import random  # Import the random module.

class Tile:
    
    def __init__ (self, pos, cell_size, type):
        # Initialize a Tile with position, size, and type.
        self.pos = pos  # Position of the tile.
        self.cell_size = cell_size  # Size of the tile.
        # Define possible types of tiles.
        self.types = ("floor", "wall", "resource", "water")
        self.current_type = type  # Current type of the tile.
        self.isObstable = False  # Flag to mark if the tile is an obstacle.
        
    def run(self):
        # Execute the display function to render the tile.
        self.display()
        
    def display(self):
        # Set the stroke color for tile borders.
        stroke(0, 50)
        
        # Change the fill color based on the tile's type.
        if(self.types[self.current_type] == "floor"):
            fill(255)  # Set fill color for floor type.
        elif(self.types[self.current_type] == "wall"):
            fill(0)  # Set fill color for wall type.
          
        # Draw the tile as a rectangle on the canvas.
        rect(self.pos.x, self.pos.y, self.cell_size, self.cell_size)
