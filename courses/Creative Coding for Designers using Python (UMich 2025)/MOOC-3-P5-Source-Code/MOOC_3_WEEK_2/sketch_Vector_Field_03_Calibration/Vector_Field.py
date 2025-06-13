from Force import Force
import random

class Vector_Field:
    # Initialize the vector field with grid dimensions and world size
    def __init__(self, cols, rows, world_x, world_y):
        self.cols = cols  # Number of columns in the grid
        self.rows = rows  # Number of rows in the grid
        self.all_forces = []  # List to store force vectors
        self.world_x = world_x  # Width of the world or canvas
        self.world_y = world_y  # Height of the world or canvas
        # Calculate cell sizes based on world dimensions and grid size
        self.cell_size_x = float(self.world_x) / self.cols
        self.cell_size_y = float(self.world_y) / self.rows
        self.max_vec_size = 17  # Maximum magnitude of force vectors
        # Check cell sizes (debugging)
        println(self.cell_size_x)
        println(self.cell_size_y)
        # Phases for noise-based animation
        self.phase_01 = 0.1
        self.phase_02 = 0.3
        
    # Populate the vector field with initial forces
    def initiate_vecfield(self):
        for i in range(self.cols):
            for j in range(self.rows):
                # Calculate position in the center of each cell
                pos = PVector(i* self.cell_size_x + self.cell_size_x/2, 
                              j*self.cell_size_y + self.cell_size_y/2)
                # Generate noise-based directions for forces
                n = noise(i*0.1, j * 0.1)
                n2 = noise(i*0.04, j * 0.04)
                # Map noise values to force vector sizes
                n = map(n, 0,1,-self.max_vec_size,self.max_vec_size)
                n2 = map(n2, 0,1,-self.max_vec_size,self.max_vec_size)
                # Create new force and add it to the list
                new_force = Force(pos, PVector(n,n2))
                self.all_forces.append(new_force)
                
    # Animate the vector field by adjusting force directions over time
    def animate_vecfield(self):
        # Increment phases to change noise values over time
        self.phase_01 += 0.01
        self.phase_02 += 0.03
        
        for i in range(self.cols):
            for j in range(self.rows):
                # Recalculate positions
                pos = PVector(i* self.cell_size_x + self.cell_size_x/2, 
                              j*self.cell_size_y + self.cell_size_y/2)
                # Adjust noise values using phases for animation
                n = noise(i*0.1 + self.phase_01, j * 0.1)
                n2 = noise(i*0.04, j * 0.04 + self.phase_02)
                # Map noise to force vector sizes
                n = map(n, 0,1,-self.max_vec_size,self.max_vec_size)
                n2 = map(n2, 0,1,-self.max_vec_size,self.max_vec_size)
                # Create new animated force and replace old forces
                new_force = Force(pos, PVector(n,n2))
                self.all_forces.append(new_force)
                
    # Run the vector field update and display
    def run(self):
        self.all_forces = []  # Clear forces to redraw updated vectors
        self.animate_vecfield()  # Update forces with animation
        self.display()  # Display updated forces
        
    # Display all forces in the vector field
    def display(self):
        for f in self.all_forces:
            f.run()  # Display each force
