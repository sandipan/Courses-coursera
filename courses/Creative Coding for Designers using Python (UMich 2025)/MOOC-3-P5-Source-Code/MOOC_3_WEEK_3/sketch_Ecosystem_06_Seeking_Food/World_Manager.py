from Food import Food  # Import the Food class from the Food module
from Herbivore import Herbivore  # Import the Herbivore class from the Herbivore module
import random  # Import the random module for generating random values

class World_Manager:
    
    def __init__(self, size_x, size_y):
        # Initialize the attributes of the World_Manager
        self.size_x = size_x
        self.size_y = size_y
        self.all_food = []  # List to store all food objects
        self.all_herbivores = []  # List to store all herbivore objects
        
        x = random.randrange(0, self.size_x)  # Generate a random x-coordinate within the world size
        y = random.randrange(0, self.size_y)  # Generate a random y-coordinate within the world size
        pos = PVector(x, y)  # Create a position vector for the new herbivore
        new_herbivore = Herbivore(pos, self.all_food)  # Create a new herbivore object
        self.all_herbivores.append(new_herbivore)  # Add the new herbivore to the list
    
    def create_food(self, rate):
        # Create food objects based on a specified rate
        if frameCount % rate == 0:  # Check if the frame count is divisible by the rate
            x = random.randrange(0, self.size_x)  # Generate a random x-coordinate within the world size
            y = random.randrange(0, self.size_y)  # Generate a random y-coordinate within the world size
            pos = PVector(x, y)  # Create a position vector for the new food
            new_food = Food(pos, 5, self.all_food)  # Create a new food object
            self.all_food.append(new_food)  # Add the new food to the list
    
    def create_herbivore(self, rate):
        # Create herbivore objects based on a specified rate
        if frameCount % rate == 0:  # Check if the frame count is divisible by the rate
            x = random.randrange(0, self.size_x)  # Generate a random x-coordinate within the world size
            y = random.randrange(0, self.size_y)  # Generate a random y-coordinate within the world size
            pos = PVector(x, y)  # Create a position vector for the new herbivore
            new_herbivore = Herbivore(pos, self.all_food)  # Create a new herbivore object
            self.all_herbivores.append(new_herbivore)  # Add the new herbivore to the list
    
    def run(self):
        # Run the simulation by creating food, running food behavior, and running herbivore behavior
        self.create_food(50)  # Create food objects
        #self.create_herbivore(120)  # Create herbivore objects
        self.run_food()  # Run food behavior
        self.run_herbivores()  # Run herbivore behavior
        
    def run_food(self):
        # Run the behavior of all food objects
        for f in self.all_food:
            f.run()
    
    def run_herbivores(self):
        # Run the behavior of all herbivore objects
        for h in self.all_herbivores:
            h.run()
