from Food import Food  # Import Food class
from Herbivore import Herbivore  # Import Herbivore class
import random

class World_Manager:
    # Initialize World Manager with canvas dimensions
    def __init__(self, size_x, size_y):
        self.size_x = size_x  # Width of the canvas
        self.size_y = size_y  # Height of the canvas
        self.all_food = []  # List to store all food objects
        self.all_herbivores = []  # List to store all herbivore objects
    
    # Create food objects at a specified rate
    def create_food(self, rate):
        if frameCount % rate == 0:  # Check frame count to determine rate
            # Generate random position for food
            x = random.randrange(0, self.size_x)
            y = random.randrange(0, self.size_y)
            pos = PVector(x, y)
            new_food = Food(pos, 5, self.all_food)  # Create new food object
            self.all_food.append(new_food)  # Add food object to the list
    
    # Create herbivore objects at a specified rate
    def create_herbivore(self, rate):
        if frameCount % rate == 0:  # Check frame count to determine rate
            # Generate random position for herbivore
            x = random.randrange(0, self.size_x)
            y = random.randrange(0, self.size_y)
            pos = PVector(x, y)
            new_herbivore = Herbivore(pos)  # Create new herbivore object
            self.all_herbivores.append(new_herbivore)  # Add herbivore object to the list
    
    # Run the simulation
    def run(self):
        self.create_food(50)  # Create food objects
        self.create_herbivore(120)  # Create herbivore objects
        self.run_food()  # Run food objects
        self.run_herbivores()  # Run herbivore objects
        
    # Update and display all food objects
    def run_food(self):
        for f in self.all_food:
            f.run()
    
    # Update and display all herbivore objects
    def run_herbivores(self):
        for h in self.all_herbivores:
            h.run()
