import random
from Particle import Particle
from Force import Force
from Vector_Field import Vector_Field

canvas_size_x = 1200  # Set canvas width
canvas_size_y = 600   # Set canvas height

all_particles = []  # List for storing particle instances
all_forces = []  # List for storing force instances (unused here)

mouse_history = []  # List for tracking mouse movement history

def setup():
    size(canvas_size_x, canvas_size_y)  # Initialize the canvas
    background(0)  # Set the background color to black
    
    global my_field  # Declare vector field globally
    my_field = Vector_Field(80, 40, canvas_size_x, canvas_size_y)  # Initialize the vector field

def draw():
    background(0)  # Clear the canvas for each draw cycle
    smooth()  # Apply smoothing for better visual appearance
    my_field.run()  # Update and display the vector field
    
    fill(255, 0, 0)  # Set fill color for highlighting
    noStroke()  # Disable stroke
    
    global highlighted, mouse_vector
    # Highlight a single vector under the mouse cursor
    highlighted = my_field.get_force(mouseX, mouseY)
    my_field.all_forces[highlighted].display_highlight(10)
    
    # Calculate mouse movement vector for use in manipulation
    mouse_vector = calc_mouse_history()
    
    # Uncomment to directly manipulate the vector field based on mouse movement
    #my_field.set_force(highlighted, mouse_vector)
    #my_field.add_force(highlighted, mouse_vector)
    
    # Update and display all particles
    for p in all_particles:
        p.run()
        
    # Manipulate adjacent vectors when left mouse button is pressed
    if mousePressed and mouseButton == LEFT:
        adjacent_vectors = my_field.get_adjacent_vectors(mouseX, mouseY, 4)  # Adjust for a specified adjacency layer
        for i in adjacent_vectors:
            my_field.all_forces[i].display_highlight(10)  # Highlight adjacent vectors
            
            diff = my_field.all_forces[i].pos.copy().sub(PVector(mouseX, mouseY))  # Calculate direction from force to mouse
            distance = diff.mag()  # Calculate distance from force to mouse
            
            factor = map(distance, 0, 100, 5.0, 0.0)  # Scale factor based on distance
            
            mouse_vector.normalize()  # Normalize mouse vector
            mouse_vector.mult(factor)  # Apply factor
            
            my_field.add_force(i, mouse_vector)  # Add manipulated vector to the field

def calc_mouse_history():
    mouse_history.append(PVector(mouseX, mouseY))  # Track mouse position
    
    if len(mouse_history) > 2:
        mouse_history.pop(0)  # Maintain a history of the last two positions
    
    if len(mouse_history) > 1:
        stroke(255)  # Set line color
        line(mouse_history[0].x, mouse_history[0].y, mouse_history[1].x, mouse_history[1].y)  # Draw line between last two positions
        
        mouse_vector = mouse_history[1].copy().sub(mouse_history[0])  # Calculate movement vector
        return mouse_vector
    else:
        return PVector(0, 0)  # Return zero vector if not enough history

# Create new particles around the mouse cursor on right click
def mouseClicked():
    if mouseButton == RIGHT:
        for i in range(100):  # Generate 100 particles
            x = mouseX + random.uniform(-100, 100)  # Random x position near mouse
            y = mouseY + random.uniform(-100, 100)  # Random y position near mouse
            new_particle = Particle(pos=PVector(x, y),
                                    world_x=canvas_size_x, 
                                    world_y=canvas_size_y, 
                                    part_list=all_particles,
                                    vector_field=my_field)
            all_particles.append(new_particle)  # Add new particle to the list
