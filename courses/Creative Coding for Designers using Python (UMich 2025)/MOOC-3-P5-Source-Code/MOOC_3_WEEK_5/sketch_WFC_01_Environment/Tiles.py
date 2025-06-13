import random  # Import the random module for potential use.

class Tile:
    # Initialize a Tile object.
    def __init__(self):
        self.name = None  # Name attribute for the tile, potentially useful for identification.
        
    def display(self, x, y, cell_size, entropy):
        # Draw the tile at a given position with a specified size.
        stroke(255, 80)  # Set stroke color with partial transparency.
        fill(0)  # Set fill color to black.
        pushMatrix()  # Save the current drawing style settings and transformations.
        translate(x, y)  # Move the origin to the specified location.
        rectMode(CORNER)  # Set the rectangle drawing mode to CORNER.
        rect(0, 0, cell_size, cell_size)  # Draw the rectangle representing the tile.
        popMatrix()  # Restore the prior drawing style settings and transformations.
    
    def display_entropy(self, x, y, cell_size, entropy):
        # Visualize the entropy value of the tile through text color and size.
        text_not_green = map(entropy, 1, 4, 0, 255)  # Map the entropy to a value for color.
        text_size = map(entropy, 1, 4, 20, 8)  # Map the entropy to a value for text size.
        
        f = createFont("Consolas-Bold-14", text_size)  # Create a font with mapped text size.
        textFont(f)  # Set the created font as the current font for text rendering.
        
        pushMatrix()  # Save the current drawing style settings and transformations.
        translate(x, y)  # Move the origin to the specified location.
        stroke(255, 80)  # Set stroke color with partial transparency.
        fill(0)  # Set fill color to black for the rectangle.
        rectMode(CORNER)  # Set the rectangle drawing mode to CORNER.
        rect(0, 0, cell_size, cell_size)  # Draw the rectangle representing the tile.
        fill(text_not_green, 255, text_not_green)  # Set fill color for the text using mapped entropy value.
        text(str(entropy), cell_size / 2 - 6, cell_size / 2 + 6)  # Display the entropy value as text.
        popMatrix()  # Restore the prior drawing style settings and transformations.
