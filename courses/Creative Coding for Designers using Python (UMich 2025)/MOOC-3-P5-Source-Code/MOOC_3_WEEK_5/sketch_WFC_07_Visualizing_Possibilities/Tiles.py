import random  # Import the random module for potential use in generating random values.

class Tile:
    # Initialize a Tile object with defined edges.
    def __init__(self, edges):
        self.edges = edges  # Store edge information in a dictionary.

    def display(self, x, y, cell_size, entropy):
        # Visual representation of the tile at a given position with specified size.
        stroke(255, 80)  # Set stroke color with partial transparency.
        fill(0)  # Set fill color to black.
        pushMatrix()  # Save the current drawing style settings and transformations.
        translate(x, y)  # Move the origin to the specified location.
        rectMode(CORNER)  # Set the rectangle drawing mode to CORNER.
        rect(0, 0, cell_size, cell_size)  # Draw the rectangle representing the tile.
        
        # Draw smaller rectangles inside the tile to represent edge information visually.
        noStroke()  # Disable stroke for inner rectangles.
        rectMode(CENTER)  # Set rectangle mode to CENTER for positioning.
        
        # Draw rectangles in different positions based on the tile's edge values.
        fill(self.color_by_edge('top'))
        rect(cell_size / 2, cell_size / 10, cell_size / 5, cell_size / 5)
        
        fill(self.color_by_edge('bottom'))
        rect(cell_size / 2, cell_size - cell_size / 10, cell_size / 5, cell_size / 5)
        
        fill(self.color_by_edge('left'))
        rect(cell_size / 10, cell_size / 2, cell_size / 5, cell_size / 5)
    
        fill(self.color_by_edge('right'))
        rect(cell_size - cell_size / 10, cell_size / 2, cell_size / 5, cell_size / 5)
        
        popMatrix()  # Restore the prior drawing style settings and transformations.
    
    def display_entropy(self, x, y, cell_size, entropy):
        # Display the entropy value of the tile through text color and size.
        text_not_green = map(entropy, 1, 4, 0, 255)  # Map the entropy to a color value.
        text_size = map(entropy, 1, 4, 20, 8)  # Map the entropy to a text size.
        
        f = createFont("Consolas-Bold-14", text_size)  # Create a font with the mapped text size.
        textFont(f)  # Apply the created font for text rendering.
        
        pushMatrix()  # Save the current drawing style settings and transformations.
        translate(x, y)  # Move the origin to the specified location.
        stroke(255, 80)  # Set stroke color with partial transparency.
        fill(0)  # Set fill color to black for the rectangle.
        rectMode(CORNER)  # Set the rectangle drawing mode to CORNER.
        rect(0, 0, cell_size, cell_size)  # Draw the rectangle representing the tile.
        fill(text_not_green, 255, text_not_green)  # Set text color using mapped entropy value.
        text(str(entropy), cell_size / 2 - 6, cell_size / 2 + 6)  # Display the entropy value as text.
        popMatrix()  # Restore the prior drawing style settings and transformations.
    
    def color_by_edge(self, which):
        # Determine the color based on the edge value.
        if self.edges[which] == 'A':
            return color(255, 0, 0)  # Red for 'A'.
        elif self.edges[which] == 'B':
            return color(0, 255, 0)  # Green for 'B'.
        else:
            return color(0)  # Black for any other value.

        
    def is_compatible(self, other, direction):
        # Determine if the current tile is compatible with another tile in a specified direction.
        if other is None:
            return True  # If there's no other tile, compatibility is assumed to be true.
        if direction == 'top':
            # For a tile to be compatible on top, its bottom edge must match the other's top edge.
            return self.edges['bottom'] == other.edges['top']
        if direction == 'bottom':
            # For a tile to be compatible on the bottom, its top edge must match the other's bottom edge.
            return self.edges['top'] == other.edges['bottom']
        if direction == 'left':
            # For a tile to be compatible on the left, its right edge must match the other's left edge.
            return self.edges['right'] == other.edges['left']
        if direction == 'right':
            # For a tile to be compatible on the right, its left edge must match the other's right edge.
            return self.edges['left'] == other.edges['right']
        return False  # If none of the conditions are met, the tiles are not compatible.
