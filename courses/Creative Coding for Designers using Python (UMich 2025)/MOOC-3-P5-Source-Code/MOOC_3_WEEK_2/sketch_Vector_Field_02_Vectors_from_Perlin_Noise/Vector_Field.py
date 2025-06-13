from Force import Force
import random

class Vector_Field:
    # Initialize vector field with specified dimensions
    def __init__(self, cols, rows):
        self.cols = cols  # Number of columns in the vector field
        self.rows = rows  # Number of rows in the vector field
        self.all_forces = []  # List to hold all forces
        self.cell_size = 40  # Size of each cell in pixels
        self.max_vec_size = 20  # Maximum size of the force vectors
        
    # Populate the vector field with forces
    def initiate_vecfield(self):
        for i in range(self.cols):
            for j in range(self.rows):
                # Calculate position based on grid and cell size
                pos = PVector(i * self.cell_size, j * self.cell_size)
                
                # Generate noise values for more natural vector directions
                n = noise(i * 0.1, j * 0.1)  # Noise for x component
                n2 = noise(i * 0.04, j * 0.04)  # Noise for y component
                # Map noise to force vector sizes
                n = map(n, 0, 1, -self.max_vec_size, self.max_vec_size)
                n2 = map(n2, 0, 1, -self.max_vec_size, self.max_vec_size)
                
                # Create new force with the noise-based direction
                new_force = Force(pos, PVector(n, n2))
                self.all_forces.append(new_force)  # Add force to the list
                
    # Run the vector field (used for updating and/or displaying)
    def run(self):
        self.display()  # Call the display method
        
    # Display all forces in the vector field
    def display(self):
        println(len(self.all_forces))  # Print the number of forces (for debugging)
        for f in self.all_forces:
            f.run()  # Display each force
