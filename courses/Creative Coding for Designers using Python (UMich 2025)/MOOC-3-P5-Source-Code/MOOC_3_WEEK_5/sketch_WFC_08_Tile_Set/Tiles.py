import random

class Tile:
    
    def __init__ (self, edges, my_image):
        # Initialize Tile object with edges and image.
        self.edges = edges  # Dictionary with keys 'top', 'bottom', 'left', 'right'.
        self.my_image = my_image  # Image to be displayed on the tile.
        
    def display(self, x, y, cell_size, entropy):
        # Display the tile with colored edges.
        
        # Draw the tile boundary.
        stroke(255,80)    
        fill(0)
        pushMatrix() 
        translate(x,y)
        rectMode(CORNER)
        rect(0, 0, cell_size, cell_size)
        
        # Draw edges.
        noStroke()
        rectMode(CENTER)
        fill( self.color_by_edge('top') )
        rect(0 + cell_size/2, 0 + cell_size/10, cell_size/5, cell_size/5)
        fill( self.color_by_edge('bottom') )
        rect(0 + cell_size/2, cell_size - cell_size/10, cell_size/5, cell_size/5)
        fill( self.color_by_edge('left') )
        rect(0 + cell_size/10, 0 + cell_size/2, cell_size/5, cell_size/5)
        fill( self.color_by_edge('right') )
        rect(cell_size - cell_size/10, 0 + cell_size/2, cell_size/5, cell_size/5)
        popMatrix()

    def display_image(self, x, y, cell_size, entropy):
        # Display the tile with an image instead of colored edges.
        
        # Draw the image on the tile.
        pushMatrix() 
        translate(x,y)
        image(self.my_image, 0, 0, cell_size, cell_size)
        popMatrix()
    
    def display_entropy(self, x, y, cell_size, entropy):
        # Display the entropy value on the tile.
        
        # Map entropy value to text color and size.
        text_not_green = map(entropy, 1,16, 0,255) 
        text_size = map(entropy, 1,16, 20, 8)#<----- be carefull to go below 0
        
        # Set text font and color.
        f = createFont("Consolas-Bold-14", text_size)
        textFont(f)
        
        # Display entropy value.
        pushMatrix() 
        translate(x,y)
        stroke(255,80)    
        fill(0)
        rectMode(CORNER)
        rect(0, 0, cell_size, cell_size)
        fill(text_not_green, 255, text_not_green)
        text(str(entropy), cell_size/2-6,cell_size/2+6)
        popMatrix()
    
    def color_by_edge(self, which):
        # Determine color based on edge value ('A' or 'B').
        if self.edges[which] == 'A':
            return color(255,0,0)  # Red for 'A'.
        elif self.edges[which] == 'B':
            return color(0,255,0)  # Green for 'B'.
        else:
            return color(0)  # Default color.
        
    def is_compatible(self, other, direction):
        # Check compatibility of edges between this tile and another tile in a given direction.
        if other is None:
            return True  # No conflict if there's no neighboring tile.
        if direction == 'top':
            return self.edges['bottom'] == other.edges['top']
        if direction == 'bottom':
            return self.edges['top'] == other.edges['bottom']
        if direction == 'left':
            return self.edges['right'] == other.edges['left']
        if direction == 'right':
            return self.edges['left'] == other.edges['right']
        return False  # Default to incompatible.
