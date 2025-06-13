import random

class Particle:
    # Particle class constructor
    def __init__(self, pos, world_x, world_y):
        # Initialize position, world dimensions, velocity, acceleration, and counter
        self.pos = pos             # Current position of the particle
        self.world_x = world_x     # Width of the world (or canvas)
        self.world_y = world_y     # Height of the world (or canvas)
        x_vel = random.uniform(-1, 1)  # Random X velocity between -1 and 1
        y_vel = random.uniform(-1, 1)  # Random Y velocity between -1 and 1
        z_vel = random.uniform(-1, 1)  # Random Z velocity between -1 and 1 (for 3D)
        self.vel = PVector(x_vel, y_vel, z_vel)  # Velocity vector
        self.acc = PVector(0, 0, 0)  # Acceleration vector (initialized to 0)
        
    # Compute the forces acting on the particle
    def compute_forces(self):
        # Get the position of the closest force
        clo_force_pos = self.force_list[self.closest_force_id].pos
        vec = self.force_list[self.closest_force_id].v_force.copy()
        dif = self.pos.copy().sub(clo_force_pos)
        
        # Calculate the force factor based on distance
        dist_to_force_sqr = dif.mag()**2
        force_factor = vec.mag() / dist_to_force_sqr
        vec.normalize()
        vec.mult(force_factor * 3)
        self.acc.add(vec)  # Add the calculated force to acceleration
    
    def closest_force(self):
        # Initialize variables to keep track of the closest force
        closest_dist = 1000000  # Set an initially high distance to compare against
        closest_id = -1         # Variable to store the index of the closest force
    
        # Loop through all the forces in the force_list
        for i in range(len(self.force_list)):
            # Calculate the difference vector between this object's position and the current force's position
            dif = self.pos.copy().sub(self.force_list[i].pos)
            # Calculate the magnitude of the difference vector, which represents the distance to the force
            dist_to_force = dif.mag()
    
            # Check if this force is closer than the previously found closest force
            if(dist_to_force < closest_dist):
                closest_dist = dist_to_force  # Update the closest distance
                closest_id = i                # Update the index of the closest force
    
        # Once the closest force is found, store it in closest_force
        closest_force = self.force_list[closest_id]
        # Update the class attribute to reflect the index of the closest force
        self.closest_force_id = closest_id


    # Method to update and display the particle each frame
    def run(self):
        self.display()  # Render particle
        self.update()   # Update particle's properties

    # Update particle's position based on its velocity
    def update(self):
        self.pos.add(self.vel)  # Add velocity to position

    # Render the particle on the canvas
    def display(self):
        stroke(255)  # Set stroke color to white
        fill(0, 0, 255)  # Set fill color to blue
        ellipse(self.pos.x, self.pos.y, 5, 5)  # Draw the particle as a small ellipse
