import random

class Particle:
    # Initialize a Particle object with position, world dimensions, particle list, and vector field
    def __init__(self, pos, world_x, world_y, part_list, vector_field):
        self.pos = pos  # Position of the particle
        self.world_x = world_x  # Width of the simulation world
        self.world_y = world_y  # Height of the simulation world
        self.lifespan = 300  # Lifespan of the particle
        # Velocity components randomly initialized
        x_vel = random.uniform(-1, 1)
        y_vel = random.uniform(-1, 1)
        self.vel = PVector(x_vel, y_vel)  # Velocity vector
        self.acc = PVector(0, 0)  # Acceleration vector
        self.count = 0  # Age of the particle
        self.gravity = PVector(0, 0.01)  # Gravity effect
        self.part_list = part_list  # List containing all particles
        self.trail = []  # Trail history for visual effect
        self.vector_field = vector_field  # Reference to the vector field affecting the particle

    def run(self):
        self.display()  # Display particle on the canvas
        self.update_trail()  # Update particle trail for visual effect
        self.move_on_field()  # Apply forces from the vector field
        self.update()  # Update particle's position and velocity
        self.border()  # Check and handle border crossing
        self.die()  # Remove particle if it has exceeded its lifespan
        
    # Apply force from vector field to particle
    def move_on_field(self):
        my_vector_index = self.vector_field.get_force(self.pos.x, self.pos.y)  # Get vector field index at particle position
        force = self.vector_field.all_forces[my_vector_index].v_force.copy()  # Copy force from vector field
        self.acc.add(force)  # Add force to particle's acceleration

    # Remove particle if it goes out of bounds
    def border(self):
        if self.pos.x <= 0 or self.pos.x >= self.world_x or self.pos.y <= 0 or self.pos.y >= self.world_y:
            self.part_list.remove(self)

    # Update the particle's trail for visualization
    def update_trail(self):
        if frameCount % 8 == 0:
            self.trail.append(self.pos.copy())
            if len(self.trail) > 15:
                self.trail.pop(0)
        
    # Update particle's velocity and position
    def update(self):
        self.vel.add(self.acc)
        self.vel.limit(3)  # Limit velocity to prevent excessive speed
        self.pos.add(self.vel)
        self.acc = PVector(0, 0)  # Reset acceleration
        
    # Check and handle the particle's death by removing it from the list
    def die(self):
        self.count += 1
        if self.count >= self.lifespan:
            self.part_list.remove(self)
    
    #Display the particles and the trails
    def display(self):
        stroke(255)  # Set the outline color of the particle to white
        fill(0, 0, 255)  # Set the fill color of the particle to blue
        ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw the particle as a small ellipse
        
        i = 0  # Initialize counter to keep track of the trail's index
        for t in self.trail:  # Iterate over each point in the particle's trail
            noStroke()  # Disable stroke for drawing trail points
            fill(255, 0, 0)  # Set fill color for trail points to red
     
            i += 1  # Increment the counter for each trail point
            if(i > 0 and i < len(self.trail)):  # Check if the current index is valid for drawing a line
                stroke(255, 0, 0, 100)  # Set the color and transparency for the trail line
                # Draw a line from the current trail point to the previous one
                line(self.trail[i].x, self.trail[i].y, self.trail[i-1].x, self.trail[i-1].y)

            
            
            
            
