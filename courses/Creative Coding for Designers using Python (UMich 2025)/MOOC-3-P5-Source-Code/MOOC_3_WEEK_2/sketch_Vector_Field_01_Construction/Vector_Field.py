from Force import Force
import random

class Vector_Field:
    # Initialize vector field with specified number of columns and rows
    def __init__(self, cols, rows):
        self.cols = cols  # Number of columns in the field
        self.rows = rows  # Number of rows in the field
        self.all_forces = []  # List to store force vectors
        self.cell_size = 40  # Size of each cell in pixels
        self.max_vec_size = 20  # Maximum magnitude of vectors
        
    # Populate the vector field with random forces
    def initiate_vecfield(self):
        for i in range(self.cols):
            for j in range(self.rows):
                pos = PVector(i * self.cell_size, j * self.cell_size)  # Position of the force
                # Random force vector components
                n = random.uniform(-1, 1) * self.max_vec_size
                n2 = random.uniform(-1, 1) * self.max_vec_size
                # Create and add new force to the field
                new_force = Force(pos, PVector(n, n2))
                self.all_forces.append(new_force)
                
    # Update and display the vector field
    def run(self):
        self.display()  # Display all forces in the field
        
    # Display all forces in the field
    def display(self):
        println(len(self.all_forces))  # Output the number of forces for debugging
        for f in self.all_forces:
            f.run()  # Run each force's display function
