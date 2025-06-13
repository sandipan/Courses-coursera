import random

class Herbivore:
    # Initialize Herbivore with position and random velocity
    def __init__(self, pos):
        self.pos = pos  # Position of the herbivore
        # Random velocity for initial movement
        self.vel = PVector(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        
    # Call move and display functions
    def run(self):
        self.move()  # Update position based on velocity
        self.display()  # Visualize the herbivore
        
    # Update position by adding velocity
    def move(self):
        self.pos.add(self.vel)
        
    # Display herbivore on canvas
    def display(self):
        noStroke()  # Disable stroke for body
        fill(100, 50, 100)  # Set color for body
        ellipse(self.pos.x, self.pos.y, 8, 8)  # Draw body as an ellipse
        
        # Draw direction arrow
        stroke(255)  # Set color for arrow
        pushMatrix()  # Save current drawing state
        translate(self.pos.x, self.pos.y)  # Move to herbivore's position
        angle = self.get_angle(self.vel)  # Calculate angle of velocity
        rotate(angle)  # Rotate drawing to align with velocity
        arrow_size = 10  # Length of the direction arrow
        # Draw arrow
        line(0, 0, arrow_size, 0)
        line(arrow_size, 0, arrow_size - 5, 5)
        line(arrow_size, 0, arrow_size - 5, -5)
        popMatrix()  # Restore drawing state
    
    # Calculate angle of a vector for rotation
    def get_angle(self, vec):
        return atan2(vec.y, vec.x)  # Return angle in radians
