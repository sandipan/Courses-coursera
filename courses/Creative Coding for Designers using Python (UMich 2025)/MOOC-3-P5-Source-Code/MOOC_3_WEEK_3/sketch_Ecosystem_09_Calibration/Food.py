class Food:
    
    def __init__(self, vec_position, f_size, all_food): 
        # Initialize Food attributes
        self.vec_position = vec_position  # Set the position vector
        self.f_size = f_size  # Set the size of the food
        self.age = 0  # Initialize age
        self.lifespan = 1200  # Set the lifespan of the food
        self.all_food = all_food  # Reference to the list containing all food objects
    
    def run(self):
        # Run the food object by executing growth and display functions
        self.grow()
        self.display()
        
    def grow(self):
        # Increment age
        self.age += 1
        
        # Remove the food object if it reaches the end of its lifespan
        if(self.age >= self.lifespan):
            self.all_food.remove(self)
    
    def remove_self(self):
        # Remove the food object from the list of all food objects
        self.all_food.remove(self)
    
    def display(self):
        # Display the food object
        g = map(self.age, 0, self.lifespan, 255,50)  # Map the color based on age
        
        fill(0, g, 0)  # Set the fill color
        noStroke()  # No stroke for drawing
        ellipse(self.vec_position.x, self.vec_position.y, self.f_size, self.f_size)  # Draw the food as an ellipse
