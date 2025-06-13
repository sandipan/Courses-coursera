import random

class Force:
    # Constructor for the Force class
    def __init__(self, pos, v_force):
        self.pos = pos          # Position of the force represented as a PVector
        self.v_force = v_force  # Vector representing the direction and magnitude of the force
    
    # Method to run the force object, which currently only displays it
    def run(self):
        self.display()
    
    # Method to display the force object on the canvas
    def display(self):
        # Draw a small green ellipse to represent the force's position
        noStroke()
        fill(255)
        ellipse(self.pos.x, self.pos.y, 5, 5)
        
        # Draw a line to represent the direction and magnitude of the force
        stroke(255)
        pushMatrix()
        # Translate to the position of the force
        translate(self.pos.x, self.pos.y)
        # Get the angle of the force vector
        angle = self.get_angle(self.v_force)
        # Rotate the canvas to align with the force vector
        rotate(angle)
        # Get the magnitude of the force vector
        v_mag = self.v_force.mag()
        # Draw the line representing the force vector
        line(0, 0, v_mag, 0)
        # Draw arrowheads at the end of the line
        line(v_mag, 0, v_mag - 5, 5)
        line(v_mag, 0, v_mag - 5, -5)
        popMatrix()
    
    # Method to calculate the angle of a vector in radians
    def get_angle(self, vec):
        # atan2() calculates the angle between the positive x-axis and the vector vec
        return atan2(vec.y, vec.x)
