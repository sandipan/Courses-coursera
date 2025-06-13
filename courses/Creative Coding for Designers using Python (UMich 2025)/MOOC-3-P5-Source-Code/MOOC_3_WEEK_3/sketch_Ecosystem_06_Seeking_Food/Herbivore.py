import random  # Import the random module for generating random values
from Node import Node  # Import the Node class from the Node module

class Herbivore:
    
    def __init__ (self, pos, all_food): #add a reference to the list of food in constructor
        self.pos = pos  # Initialize the position of the Herbivore
        self.vel = PVector(random.uniform(-0.5,0.5),random.uniform(-0.5,0.5))  # Initialize the velocity of the Herbivore with random values
        self.isAwake = True  # Initialize the awake state of the Herbivore
        self.isHungry = False  # Initialize the hungry state of the Herbivore
        self.isTired = False  # Initialize the tired state of the Herbivore
        self.current_node = self.build_decision_tree()  # Initialize the decision tree of the Herbivore
        self.hunger_level = 0  # Initialize the hunger level of the Herbivore
        self.hunger_threshold = 100  # Set the hunger threshold for the Herbivore
        self.rest_level = 0  # Initialize the rest level of the Herbivore
        self.rest_threshold = 100  # Set the rest threshold for the Herbivore
        
        self.wander_states = ("IDLE","MOVING","ROTATING")  # Define wander states for the Herbivore
        self.current_wander_state = 0  # Initialize the current wander state index
        self.action_duration = 200  # Set the default action duration
        self.action_count = 0  # Initialize the action count
        
        self.all_foods = all_food  # Initialize list of food

    def run(self):
        # Display the Herbivore
        self.display()
        # Execute the message function of the current node in the decision tree
        self.current_node.message()
        # Update the current node based on conditions or actions
        self.update_current_node()
        
    def update_current_node(self):
        # Update the current node based on conditions or actions
        if self.current_node.condition_var is not None:  # If the current node has a condition variable
            if self.current_node.condition_var:  # If the condition is true
                self.current_node = self.current_node.yesNode  # Move to the yesNode
            else: 
                self.current_node = self.current_node.noNode  # Move to the noNode
        elif self.current_node.action is not None:  # If the current node has an action
            # Execute the action function associated with the current node
            self.current_node.action_func()
            
            
    def build_decision_tree(self):
        # Create leaf nodes for different actions with associated action functions
        leaf1 = Node(name="l1", action="Wander", action_func=self.wander)
        leaf2 = Node(name="l2", action="Seek Food", action_func=self.seek_food)
        leaf3 = Node(name="l3", action="Rest", action_func=self.rest)
        
        # Create condition nodes with associated condition variables and child nodes
        node1 = Node(name="n1", condition="Is Hungry?", yesNode=leaf2, noNode=leaf1, condition_var=self.isHungry)
        #node2 = Node(name="n2", condition="Is Tired?", yesNode=leaf3, noNode=leaf1, condition_var=self.isTired)
        
        # Create the root node of the decision tree
        root = Node(name="root", condition="Is Awake?", yesNode=node1, noNode=leaf3, condition_var=self.isAwake)
        
        return root
    
    def wander(self):
        # Execute wandering behavior
        self.wander_actions()  # Execute wandering actions
        self.hunger_level += 1  # Increase hunger level
        if self.hunger_level > self.hunger_threshold:  # Check if hunger level exceeds threshold
            self.isHungry = True  # Set herbivore as hungry
            self.current_node = self.build_decision_tree()  # Rebuild decision tree
    
    def wander_actions(self):
        # Execute actions based on current wander state
        if self.wander_states[self.current_wander_state] == "IDLE":  # Check if in idle state
            self.trigger_action_change()  # Trigger action change
        elif self.wander_states[self.current_wander_state] == "MOVING":  # Check if in moving state
            self.move()  # Move
            self.trigger_action_change()  # Trigger action change
        elif self.wander_states[self.current_wander_state] == "ROTATING":  # Check if in rotating state
            self.new_rotation()  # Rotate
            self.next_wander_state()  # Move to next wander state
        else:
            println("No action")  # If no valid action, print a message

    
    def idle(self):
        # Increment action count
        self.action_count += 1
    
    def trigger_action_change(self):    
        # Increment action count and check if action duration exceeded
        self.action_count += 1
        if self.action_count > self.action_duration:
            self.next_wander_state()  # Move to next wander state
            self.action_count = 0  # Reset action count
            self.action_duration = random.randrange(150, 250)  # Set new action duration
    
    def next_wander_state(self):
        # Move to next wander state and reset if exceeded
        self.current_wander_state += 1
        if self.current_wander_state > 2:
            self.current_wander_state = 0
            
    def new_rotation(self):
        # Generate a new random angle and rotate velocity vector
        new_angle = random.uniform(0, 360)
        self.vel = self.rotate_vector(self.vel, new_angle)
        
    def rotate_vector(self, v, angle):
        # Rotate a vector by a given angle
        angle = radians(angle)
        x = v.x * cos(angle) - v.y * sin(angle)
        y = v.x * sin(angle) + v.y * cos(angle)
        return PVector(x, y)

    def rest(self):
        # Print resting message
        println("resting")
        # Increment rest level
        self.rest_level += 1
        if self.rest_level > self.rest_threshold:
            # Set awake state and rebuild decision tree if rest threshold exceeded
            self.isAwake = True
            self.current_node = self.build_decision_tree()
        
    def seek_food(self):
        # Print seeking food message
        println("seeking food")
        
        # Find the closest food
        closest_food = self.find_closest_food()
        # Look towards the closest food
        self.look_towards(closest_food.vec_position)
        # Move towards it
        self.move()
        
        # Eat it
        # Transition back to not hungry  - self.isHungry = False
        # Transition to resting - self.isAwake = True
    
    def find_closest_food(self):
        # Initialize variables
        closest_dist = 10000000
        closest_id = -1
        # Iterate through all foods to find the closest one
        for i, food in enumerate(self.all_foods):
            diff = self.pos.copy().sub(food.vec_position)
            distance = diff.mag()
            if distance < closest_dist:
                closest_dist = distance
                closest_id = i
        # Get the closest food
        closest_food = self.all_foods[closest_id] 
        # Draw a line to the closest food for visualization
        stroke(255,50)   
        line(self.pos.x, self.pos.y, closest_food.vec_position.x, closest_food.vec_position.y)
                
        return closest_food

    def look_towards(self, target_vector):
        # Calculate the difference between the target vector and current position
        dif = target_vector.copy().sub(self.pos)
        # Get the current velocity magnitude
        current_magnitud = self.vel.mag()
        # Normalize the difference vector
        dif.normalize()
        # Scale the difference vector by the current magnitude of velocity
        dif.mult(current_magnitud)
        
        # Set the velocity to the difference vector
        self.vel = dif
    
    def move(self):
        # Move the object by adding velocity to position
        self.pos.add(self.vel)
    
    def display(self):
        # Display the object
        noStroke()
        fill(100,50,100)
        ellipse(self.pos.x, self.pos.y, 8, 8)
        
        stroke(255)
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        angle = self.get_angle(self.vel)
        rotate(angle)
        arrow_size = 10
        line(0,0,arrow_size,0)
        line(arrow_size,0,arrow_size-5,5)
        line(arrow_size,0,arrow_size-5,-5)
        popMatrix()
    
    def get_angle(self, vec):
        # Calculate and return the angle of the vector
        return atan2(vec.y, vec.x)

    
