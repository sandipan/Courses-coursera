import random  # Import the random module for generating random values
from Node import Node  # Import the Node class from the Node module

class Herbivore:
    
    def __init__ (self, pos, all_food):
        # Initialize Herbivore attributes
        self.pos = pos  # Set the position of the Herbivore
        self.vel = PVector(random.uniform(-0.5,0.5),random.uniform(-0.5,0.5))  # Set the velocity of the Herbivore with random values
        self.isAwake = True  # Set the awake state of the Herbivore
        self.isHungry = False  # Set the hungry state of the Herbivore
        self.isTired = False  # Set the tired state of the Herbivore
        self.current_node = self.build_decision_tree()  # Build the decision tree for the Herbivore
        self.hunger_level = 0  # Initialize the hunger level of the Herbivore
        self.hunger_threshold = 1200  # Set the hunger threshold of the Herbivore
        self.rest_level = 0  # Initialize the rest level of the Herbivore
        self.rest_threshold = 200  # Set the rest threshold of the Herbivore
        
        self.wander_states = ("IDLE","MOVING","ROTATING")  # Define wander states
        self.current_wander_state = 0  # Initialize the current wander state
        self.action_duration = 200  # Set the duration of actions
        self.action_count = 0  # Initialize the action count
        
        self.all_foods = all_food  # Reference to the list containing all food objects

    def run(self):
        # Run the Herbivore by executing display, message, and update functions
        #self.move()
        self.display()
        self.current_node.message()
        self.update_current_node()
        
    def update_current_node(self):
        # Update the current node based on conditions or actions
        
        if self.current_node.condition_var is not None:  # If the current node has a condition variable
            if self.current_node.condition_var:  # If the condition is true
                self.current_node = self.current_node.yesNode  # Move to the yesNode
            else: 
                self.current_node = self.current_node.noNode  # Move to the noNode
        elif self.current_node.action is not None:  # If the current node has an action
            #println("Animal will: " + self.current_node.action)
            self.current_node.action_func()  # Execute the action function

        
    def build_decision_tree(self):
        # Build the decision tree for Herbivore behavior
        
        # Create leaf nodes for different actions
        leaf1 = Node(name="l1", action="Wander", action_func=self.wander)
        leaf2 = Node(name="l2", action="Seek Food", action_func=self.seek_food)
        leaf3 = Node(name="l3", action="Rest", action_func=self.rest)
        
        # Create condition nodes
        node1 = Node(name="n1", condition="Is Hungry?", yesNode=leaf2, noNode=leaf1, condition_var=self.isHungry)
        #node2 = Node(name="n2", condition="Is Tired?", yesNode=leaf3, noNode=leaf1, condition_var=self.isTired)
        
        # Create the root node
        root = Node(name="root", condition="Is Awake?", yesNode=node1, noNode=leaf3, condition_var=self.isAwake)
        
        return root  # Return the root node of the decision tree
    
    def wander(self):
        # Perform wandering behavior
        
        println("wandering, hunger: " + str(self.hunger_level) + "," + str(self.isHungry) )
        self.wander_actions()
        self.hunger_level += 1
        if self.hunger_level > self.hunger_threshold:
            self.isHungry = True
            self.current_node = self.build_decision_tree()  # Rebuild decision tree when hungry
    
    def wander_actions(self):
        # Execute wander actions based on the current wander state
        
        println(self.wander_states[self.current_wander_state] + ", " + str(self.action_count) + "/" + str(self.action_duration) )
        if self.wander_states[self.current_wander_state] == "IDLE":
            #self.idle()
            self.trigger_action_change()
        elif self.wander_states[self.current_wander_state] == "MOVING":
            self.move(1)  # Move with a factor of 1
            self.trigger_action_change()
        elif self.wander_states[self.current_wander_state] == "ROTATING":
            self.new_rotation()
            self.next_wander_state()
        else:
            println("No action") # No action if no valid state

    def idle(self):
        # Increment action count
        self.action_count += 1
    
    def trigger_action_change(self):    
        # Increment action count and change state if duration is exceeded
        self.action_count += 1
        if self.action_count > self.action_duration:
            self.next_wander_state()
            self.action_count = 0
            self.action_duration = random.randrange(150, 250)  # Set a new random action duration
    
    def next_wander_state(self):
        # Move to the next wander state, loop back to the beginning if exceeding available states
        self.current_wander_state += 1
        if self.current_wander_state > 2:
            self.current_wander_state = 0
            
    def new_rotation(self):
        # Generate a new random angle for rotation
        new_angle = random.uniform(0, 360)
        # Rotate the velocity vector by the new angle
        self.vel = self.rotate_vector(self.vel, new_angle)
        
    def rotate_vector(self, v, angle):
        # Rotate a vector by a given angle
        angle = radians(angle)
        x = v.x * cos(angle) - v.y * sin(angle)
        y = v.x * sin(angle) + v.y * cos(angle)
        return PVector(x, y)
    
    def rest(self):
        # Perform resting behavior
        
        println("resting")
        # Increment rest level
        self.rest_level += 1
        if self.rest_level > self.rest_threshold:
            # Transition to awake state when rest threshold is exceeded
            self.isAwake = True
            self.current_node = self.build_decision_tree()  # Rebuild decision tree after resting

        
    def seek_food(self):
        # Print message indicating seeking food
        println("seeking food")
        
        # Find the closest food
        closest_food = self.find_closest_food()  # Find the closest food
        # Look towards the closest food
        self.look_towards(closest_food.vec_position)
        # Move towards the food
        self.move(3)
        
        # Eat the food if in range, reset hunger, set not hungry, and go to sleep
        self.eat_food_in_range(closest_food, 5)

    def eat_food_in_range(self, closest_food, eat_range):
        # Calculate distance to the food
        diff = closest_food.vec_position.copy().sub(self.pos)
        distance = diff.mag()
        
        # If within eating range, eat the food and update states
        if distance < eat_range:
            closest_food.remove_self()  # Remove the food
            self.hunger_level = 0  # Reset hunger level
            self.isHungry = False  # Set not hungry
            self.isAwake = False  # Go to sleep
            self.current_node = self.build_decision_tree()  # Rebuild decision tree
    
    def find_closest_food(self):
        # Find the closest food item among all available foods
        closest_dist = 10000000
        closest_id = -1
        for i, food in enumerate(self.all_foods):
            # Calculate distance to current food
            diff = self.pos.copy().sub(food.vec_position)
            distance = diff.mag()
            # Update closest food if closer
            if distance < closest_dist:
                closest_dist = distance
                closest_id = i
        # Retrieve the closest food
        closest_food = self.all_foods[closest_id] 
        # Draw a line to the closest food for visualization
        stroke(255, 50)   
        line(self.pos.x, self.pos.y, closest_food.vec_position.x, closest_food.vec_position.y)
                
        return closest_food

    
    def look_towards(self, target_vector):
        # Calculate the difference between the target and current position
        diff = target_vector.copy().sub(self.pos)
        current_magnitude = self.vel.mag()  # Get current velocity magnitude
        diff.normalize()  # Normalize the difference vector
        diff.mult(current_magnitude)  # Scale the difference vector
        
        # Set the velocity to the adjusted difference vector
        self.vel = diff

    def move(self, factor):
        # Normalize velocity vector and scale by given factor
        self.vel.normalize()
        self.vel.mult(factor)
        self.pos.add(self.vel)  # Move the object by the scaled velocity
    
    def display(self):
        # Draw the object
        noStroke()  # No outline
        fill(100, 50, 100)  # Fill color
        ellipse(self.pos.x, self.pos.y, 8, 8)  # Draw an ellipse
        
        # Draw a directional arrow
        stroke(255)  # Arrow color
        pushMatrix()  # Save the current transformation matrix
        translate(self.pos.x, self.pos.y)  # Translate to the object's position
        angle = self.get_angle(self.vel)  # Get the angle of the velocity vector
        rotate(angle)  # Rotate by the angle
        arrow_size = 10  # Size of the arrow
        line(0, 0, arrow_size, 0)  # Draw the line of the arrow
        line(arrow_size, 0, arrow_size - 5, 5)  # Draw the first segment of the arrow
        line(arrow_size, 0, arrow_size - 5, -5)  # Draw the second segment of the arrow
        popMatrix()  # Restore the previous transformation matrix

    def get_angle(self, vec):
        # Calculate the angle of the vector
        return atan2(vec.y, vec.x)  # Return the angle using atan2

    
