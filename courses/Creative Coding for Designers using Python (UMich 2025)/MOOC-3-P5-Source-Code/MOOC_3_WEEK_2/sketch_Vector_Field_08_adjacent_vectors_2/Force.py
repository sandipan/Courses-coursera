import random

class Force:
    # Initialize a Force object with a position and a vector force
    def __init__(self, pos, v_force):
        self.pos = pos  # Position of the force
        self.v_force = v_force  # Vector representing the direction and magnitude of the force

    # Run the display function to visualize the force
    def run(self):
        self.display()

    # Visualize the force vector
    def display(self):
        noStroke()  # Do not draw a stroke for the ellipse
        fill(255)  # Set fill color to white
        #ellipse(self.pos.x, self.pos.y, 5, 5)  # Commented out: Draw a small ellipse at the force's position

        stroke(255)  # Set stroke color to white for the line
        pushMatrix()  # Save the current drawing state
        translate(self.pos.x, self.pos.y)  # Translate to the force's position
        angle = self.get_angle(self.v_force)  # Calculate the angle of the force vector
        rotate(angle)  # Rotate the drawing context to align with the force vector
        v_mag = self.v_force.mag()  # Get the magnitude of the force vector
        line(0, 0, v_mag, 0)  # Draw a line representing the force vector
        #line(v_mag, 0, v_mag-3, 3)  # Commented out: Draw lines for an arrowhead
        #line(v_mag, 0, v_mag-3, -3)
        popMatrix()  # Restore the previous drawing state

    # Highlight the force with a highlighted square
    def display_highlight(self, h_size):
        stroke(255)  # Set stroke color to white for the highlight
        noFill()  # Do not fill the rectangle
        rectMode(CENTER)  # Draw the rectangle from its center
        rect(self.pos.x, self.pos.y, h_size, h_size)  # Draw a square centered on the force's position

    # Calculate the angle of the vector for use in rotation
    def get_angle(self, vec):
        return atan2(vec.y, vec.x)  # Return the angle between the vector and the x-axis
