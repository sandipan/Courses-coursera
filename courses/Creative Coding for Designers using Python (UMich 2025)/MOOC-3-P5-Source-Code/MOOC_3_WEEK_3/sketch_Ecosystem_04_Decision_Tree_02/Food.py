class Food:
    # Initialize food properties
    def __init__(self, vec_position, f_size, all_food): 
        self.vec_position = vec_position  # Position of food
        self.f_size = f_size  # Size of food
        self.age = 0  # Age of food
        self.lifespan = 400  # Lifespan of food
        self.all_food = all_food  # Reference to all food in the environment
    
    # Handle growth and display of food
    def run(self):
        self.grow()  # Increase age and check for removal
        self.display()  # Visualize food
        
    # Increase age of food and remove if past lifespan
    def grow(self):
        self.age += 1  # Increase age
        
        if(self.age >= self.lifespan):  # Check if past lifespan
            self.all_food.remove(self)  # Remove from all food list
    
    # Display food on canvas
    def display(self):
        g = map(self.age, 0, self.lifespan, 255, 50)  # Calculate green color based on age
        
        fill(0, g, 0)  # Set color
        noStroke()  # Disable stroke for a cleaner look
        ellipse(self.vec_position.x, self.vec_position.y, self.f_size, self.f_size)  # Draw food as ellipse
