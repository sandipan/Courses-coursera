import random  # Import the random module for generating random values
from Node import Node  # Import the Node class from the Node module

class Herbivore:
    
    def __init__ (self, pos):
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
        # Print a message indicating the Herbivore is wandering
        println("wandering, hunger: " + str(self.hunger_level))
        # Execute the actions associated with wandering
        self.wander_actions()
        # Increment the hunger level of the Herbivore
        self.hunger_level += 1
        # Set the Herbivore as hungry if the hunger level exceeds the threshold
        if self.hunger_level > self.hunger_threshold:
            self.isHungry = True

    def wander_actions(self):
        # Print the current state of wandering along with action count and duration
        println(self.wander_states[self.current_wander_state] + ", " + str(self.action_count) + "/" + str(self.action_duration))
        # Execute corresponding action based on current wander state
        if self.wander_states[self.current_wander_state] == "IDLE":
            # Execute the idle action
            #self.idle()
            self.trigger_action_change()
        elif self.wander_states[self.current_wander_state] == "MOVING":
            # Execute the move action
            self.move()
            self.trigger_action_change()
        elif self.wander_states[self.current_wander_state] == "ROTATING":
            # Execute the rotation action
            self.new_rotation()
            self.next_wander_state()
        else:
            # Print a message indicating no action
            println("No action")
    
    def idle(self):
        # Increment the action count for idling
        self.action_count += 1
    
    def trigger_action_change(self):    
        # Increment the action count and change the wander state if the action count exceeds the duration
        self.action_count += 1
        if self.action_count > self.action_duration:
            self.next_wander_state()
            self.action_count = 0
            self.action_duration = random.randrange(150, 250)
    
    def next_wander_state(self):
        # Move to the next wander state, reset to the first state if exceeding the last state
        self.current_wander_state += 1
        if self.current_wander_state > 2:
            self.current_wander_state = 0
        
    
    def new_rotation(self):
        # Generate a new random angle for rotation
        new_angle = random.uniform(0, 360)
        # Rotate the velocity vector by the new angle
        self.vel = self.rotate_vector(self.vel, new_angle)
        
    def rotate_vector(self, v, angle):
        # Convert the angle to radians
        angle = radians(angle)
        # Compute the new x and y components after rotation
        x = v.x * cos(angle) - v.y * sin(angle)
        y = v.x * sin(angle) + v.y * cos(angle)
        # Return the rotated vector as a PVector
        return PVector(x, y)
    
    def rest(self):
        # Print a message indicating resting
        println("resting")
        # Increment the rest level
        self.rest_level += 1
        # If the rest level exceeds the threshold, set the herbivore awake
        if self.rest_level > self.rest_threshold:
            self.isAwake = True

    #To be completed in next example
    def seek_food(self):
        println("seeking food")
        #Find the closest food
        #Move towards it
        #Eat it
        #Transition back to not hungry  - self.isHungry = False
        #Transition to resting - self.isAwake = True
        
    def move(self):
        # Move the herbivore by adding its velocity vector to its position
        self.pos.add(self.vel)
    
    def display(self):
        # Display the herbivore as an ellipse with an arrow representing its direction
        noStroke()  # No stroke for the ellipse
        fill(100, 50, 100)  # Fill color for the ellipse
        ellipse(self.pos.x, self.pos.y, 8, 8)  # Draw the herbivore as an ellipse
        
        stroke(255)  # Stroke color for the arrow
        pushMatrix()  # Push the current transformation matrix onto the stack
        translate(self.pos.x, self.pos.y)  # Translate to the position of the herbivore
        angle = self.get_angle(self.vel)  # Get the angle of the velocity vector
        rotate(angle)  # Rotate by the angle
        arrow_size = 10  # Size of the arrow
        line(0, 0, arrow_size, 0)  # Draw the line of the arrow
        line(arrow_size, 0, arrow_size - 5, 5)  # Draw the first segment of the arrow
        line(arrow_size, 0, arrow_size - 5, -5)  # Draw the second segment of the arrow
        popMatrix()  # Pop the current transformation matrix from the stack
    
    def get_angle(self, vec):
        # Calculate the angle of the vector
        return atan2(vec.y, vec.x)  # Return the angle using atan2
    
