import random

class Force:
    # Initialize a force with a position and a vector
    def __init__(self, pos, v_force):
        self.pos = pos  # Position of the force
        self.v_force = v_force  # Vector representing the force's direction and magnitude
        
    # Method to run the force's behaviors
    def run(self):
        self.display()  # Display the force on the canvas
        
    # Display the force vector visually
    def display(self):
        noStroke()  # Do not draw an outline for shapes
        fill(255)  # Set fill color to white
        # Drawing of the force's position is commented out
        #ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw an ellipse at the force's position
        
        stroke(255)  # Set stroke color to white for drawing lines
        pushMatrix()  # Save the current drawing state
        translate(self.pos.x, self.pos.y)  # Move the origin to the force's position
        angle = self.get_angle(self.v_force)  # Calculate the angle of the force vector
        rotate(angle)  # Rotate the drawing context by the angle of the force
        v_mag = self.v_force.mag()  # Calculate the magnitude of the force vector
        line(0, 0, v_mag, 0)  # Draw a line representing the force vector
        # Arrowhead lines are commented out; to visualize the direction, uncomment these lines
        #line(v_mag, 0, v_mag-3, 3)
        #line(v_mag, 0, v_mag-3, -3)
        popMatrix()  # Restore the previous drawing state
    
    # Calculate the angle of the vector for rotation
    def get_angle(self, vec):
        return atan2(vec.y, vec.x)  # Return the angle in radians between the x-axis and the vector
