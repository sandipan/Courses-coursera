from Food import Food 
import random

class World_Manager:
    # Initialize world with dimensions and empty food list
    def __init__(self, size_x, size_y):
        self.size_x = size_x  # World width
        self.size_y = size_y  # World height
        self.all_food = []  # List to store all food instances
    
    # Generate food at a given rate
    def create_food(self, rate):
        if(frameCount % rate == 0):  # Check if it's time to create new food
            x = random.randrange(0, self.size_x)  # Random x within world
            y = random.randrange(0, self.size_y)  # Random y within world
            pos = PVector(x, y)  # Position for new food
            new_food = Food(pos, 5, self.all_food)  # Create new food instance
            self.all_food.append(new_food)  # Add new food to list
    
    # Update and display food
    def run(self):
        self.create_food(50)  # Attempt to create food every 50 frames
        self.run_food()  # Update and display all food
    
    # Iterate through and update all food instances
    def run_food(self):
        for f in self.all_food:
            f.run()  # Update and display each food instance
