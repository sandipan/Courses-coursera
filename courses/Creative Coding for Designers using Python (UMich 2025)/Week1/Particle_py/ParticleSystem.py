import random
from Particle import Particle  # Importing the Particle class

# Canvas dimensions
canvas_size_x = 1200
canvas_size_y = 600

all_particles = []  # List to hold all particle objects
all_forces = []  
mouse_history = [] 

'''
def setup():
    # Create a canvas with the specified width and height
    size(canvas_size_x, canvas_size_y)
    
    background(0)  # Set the background color to black
    
    # Create 100 particles
    for i in range(100):
        x = 600  # Set a fixed x-coordinate for all particles
        y = 300  # Set a fixed y-coordinate for all particles
        # Create a new Particle object at (x, y)
        new_particle = Particle(PVector(x, y), canvas_size_x, canvas_size_y)
        all_particles.append(new_particle)  # Add the new particle to the list
    
def draw():
    background(0)  # Clear the canvas with a black background on each frame
    
    # Update and draw each particle
    for p in all_particles:
        p.run()  # Call the run method of each particle
'''

'''
# Set up the Processing sketch
def setup():
    size(400, 400)  # Define the size of the canvas
'''

def setup():
    # Create a canvas with the specified width and height
    size(canvas_size_x, canvas_size_y)    
    background(0)  # Set the background color to black
    smooth()
    
    global my_field
    my_field = VectorField(80, 40, canvas_size_x, canvas_size_y)
    my_field.initiate_vecfield()      

def draw():
    background(0)  # Clear the canvas with a black background on each frame
    my_field.run()
    # Update and draw each particle
    #for p in all_particles:
    #    p.run()  # Call the run method of each particle
    #highlighted = my_field.get_force(mouseX, mouseY)
    #if o <= index < len(self.all_forces):
    #    return index
    #else:
    #    return IndexError("Vector index out of range")
    #my_field.all_forces[highlighted].display_highlight(10)
    
'''
# Called repeatedly to draw the sketch
def draw():
    background(255)  # Set the background color to white
    # Loop through a grid of points on the canvas
    for y in range(0, height, 20):
        for x in range(0, width, 20):
            # Calculate an angle using Perlin noise for smooth variation
            angle = noise(x * 0.01, y * 0.01) * TWO_PI
            # Create a vector pointing in the direction of the angle
            v = PVector(cos(angle), sin(angle))
            # Draw the vector as an arrow at point (x, y)
            drawVector(v, x, y)
'''

# Function to draw a vector as a line with an arrowhead
def drawVector(v, x, y):
    pushMatrix()  # Save the current transformation matrix
    translate(x, y)  # Move the origin to (x, y)
    rotate(v.heading())  # Rotate the canvas to align with the vector's direction
    line(0, 0, 10, 0)  # Draw a line representing the vector
    popMatrix()  # Restore the original transformation matrix
 
# Function to calculate and maintain a history of mouse positions
def calc_mouse_history():
    # Append the current mouse position as a PVector to the mouse_history list
    mouse_history.append(PVector(mouseX, mouseY))
    
    # If the length of mouse_history exceeds 2, remove the oldest entry
    if len(mouse_history) > 2:
        mouse_history.pop(0)
    
    # If there are at least two points in mouse_history, draw a line between them
    if len(mouse_history) > 1:
        stroke(255)  # Set the stroke color to white
        # Draw a line between the first and second points in the mouse history
        line(mouse_history[0].x, mouse_history[0].y,
             mouse_history[1].x, mouse_history[1].y)
