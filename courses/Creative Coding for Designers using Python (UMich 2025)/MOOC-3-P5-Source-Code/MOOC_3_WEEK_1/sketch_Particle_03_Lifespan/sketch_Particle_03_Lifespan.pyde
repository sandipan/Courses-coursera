import random
from Particle import Particle  # Import the Particle class to use for creating particle objects

# Canvas dimensions specified as global variables
canvas_size_x = 1200  # Width of the canvas
canvas_size_y = 600   # Height of the canvas

all_particles = []  # List to store all particle objects created

def setup():
    # Create a canvas with the specified width and height
    size(canvas_size_x, canvas_size_y)
    
    # Set the background color to black (0)
    background(0)
    
    
def draw(): 
    # Clear the canvas with a black background each time draw() is called
    background(0)
    
    # Create 4 new particles at the current mouse position each frame
    for i in range(4):
        x = mouseX  # Current horizontal position of the mouse
        y = mouseY  # Current vertical position of the mouse
        
        # Create a new particle at the mouse position
        new_particle = Particle(PVector(x, y), canvas_size_x, canvas_size_y, all_particles)
        
        # Add the newly created particle to the list of all particles
        all_particles.append(new_particle)
    
    # Iterate through all particles and call their run method
    # The run method is expected to handle particle behavior such as movement and display
    for p in all_particles:
        p.run()
