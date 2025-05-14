
# coding: utf-8

# # Introduction To GradCAM (Part 1) - Lecture Notebook

# In this lecture notebook we'll be looking at an introduction to Grad-CAM, a powerful technique for interpreting Convolutional Neural Networks. Grad-CAM stands for Gradient-weighted Class Activation Mapping.
# 
# CNN's are very flexible models and their great predictive power comes at the cost of losing interpretability (something that is true for all Artificial Neural Networks). Grad-CAM attempts to solve this by giving us a graphical visualisation of parts of an image that are the most relevant for the CNN when predicting a particular class.
# 
# Aside from working on some Grad-CAM concepts we'll also look at how we can use Keras to access some concrete information of our model. Let's dive into it!

# In[1]:


import keras
from keras import backend as K
from util import *


# The `load_C3M3_model()` function has been taken care of and its internals are out of the scope of this notebook. But if it intrigues you, you can take a look at it in `util.py` 

# In[2]:


# Load the model we are going to be using
model = load_C3M3_model()


# As you may already know, we can check the architecture of our model using the `summary()` method. 
# 
# After running the code block below we’ll see that this model has a lot of layers. One advantage of Grad-CAM over previous attempts of interpreting CNN's (such as CAM) is that it is architecture agnostic. This means it can be used for CNN's with complex architectures such as this one:

# In[3]:


# Print all of the model's layers
model.summary()


# Keras models include abundant information about the elements that make them up. You can check all of the available methods and attributes of this class by using the `dir()` method:

# In[4]:


# Printing out methods and attributes for Keras model
print(f"Keras' models have the following methods and attributes: \n\n{dir(model)}")


# Wow, this certainly is a lot! These models are indeed very complex. 
# 
# What we are interested in are the layers of the model which can be easily accessed as an attribute using the dot notation. They are a list of layers, which can be confirmed by checking its type:

# In[5]:


# Check the type of the model's layers
type(model.layers)


# In[6]:


# Print 5 first layers along with their names
for i in range(5):
    l = model.layers[i]
    print(f"Layer number {i}: \n{l} \nWith name: {l.name} \n")


# Let's check how many layers our model has:

# In[7]:


# Print number of layers in our model
print(f"The model has {len(model.layers)} layers")


# Our main goal is interpreting the representations which the neural net is creating for classifying our images. But as you can see this architecture has many layers. 
# 
# Actually we are really interested in the representations that the convolutional layers produce because these are the layers that (hopefully) recognize concrete elements within the images. We are also interested in the "concatenate" layers because in our model's arquitecture they concatenate convolutional layers.
# 
# Let's check how many of those we have:

# In[8]:


# Number of layers that are of type "Convolutional" or "Concatenate"
len([l for l in model.layers if ("conv" in str(type(l))) or ("Concatenate" in str(type(l)))])


# This number is still very big to try to interpret each one of these layers individually. 
# 
# One characteristic of CNN's is that the earlier layers capture low-level features such as edges in an image while the deeper layers capture high-level concepts such as physical features of a "Cat". 
# 
# Because of this **Grad-CAM usually focuses on the last layers, as they provide a better picture of what the network is paying attention to when classifying a particular class**. Let's grab the last concatenate layer of our model. Luckily Keras API makes this quite easy:

# In[9]:


# Save the desired layer in a variable
layer = model.layers[424]

# Print layer
layer


# This approach is not the best since we will need to know the exact index of the desired layer. Luckily we can use the `get_layer()` method in conjunction with the layer's name to get the same result. 
# 
# Remember you can get the name from the information displayed earlier with the `summary()` method.

# In[10]:


# Save the desired layer in a variable
layer = model.get_layer("conv5_block16_concat")

# Print layer
layer


# Let's check what methods and attributes we have available when working with this layer:

# In[11]:


# Printing out methods and attributes for Keras' layer
print(f"Keras' layers have the following methods and attributes: \n\n{dir(layer)}")


# Since we want to know the representations which this layer is abstracting from the images we should be interested in the output from this layer. Luckily we have this attribute available:

# In[12]:


# Print layer's output
layer.output


# Do you notice something odd? The shape of this tensor is undefined for some dimensions. This is because this tensor is just a placeholder and it doesn't really contain information about the activations that occurred in this layer. 
# 
# To compute the actual activation values given an input we will need to use a **Keras function**.
# 
# This function accepts lists of input and output placeholders and can be used with an actual input to compute the respective output of the layer associated to the placeholder for that given input. 
# 
# Before jumping onto the Keras function we should rewind a little bit to get the placeholder tensor associated with the input. You can get this from the model’s input:

# In[13]:


# Print model's input tensor placeholder
model.input


# We can see that this is a placeholder as well. Now let's instantiate our Keras function using Keras backend. Please be aware that this **function expects its arguments as lists or tuples**:

# In[14]:


# Instantiate the function to compute the activations of the last convolutional layer
last_layer_activations_function = K.function([model.input], [layer.output])

# Print the Keras function
last_layer_activations_function


# Let's test the functions for computing the last layer activation which we just defined on a particular image. Don't worry about the code to load the image, this has been taken care of for you. You should only care that an image ready to be processed will be saved in the x variable:

# In[15]:


# Load dataframe that contains information about the dataset of images
df = pd.read_csv("nih_new/train-small.csv")

# Path to the actual image
im_path = 'nih_new/images-small/00000599_000.png'

# Load the image and save it to a variable
x = load_image(im_path, df, preprocess=False)

# Display the image
plt.imshow(x, cmap = 'gray')
plt.show()


# We should normalize this image before going forward, this has also been taken care of:

# In[16]:


# Calculate mean and standard deviation of a batch of images
mean, std = get_mean_std_per_batch(df)

# Normalize image
x = load_image_normalize(im_path, mean, std)


# Now we have everything we need to compute the actual values of the last layer activations. In this case we should also **provide the input as a list or tuple**:

# In[17]:


# Run the function on the image and save it in a variable
actual_activations = last_layer_activations_function([x])


# An important intermediary step is to trim the batch dimension which can be done like this. This is necessary because we are applying Grad-CAM to a single image rather than to a batch of images:

# In[18]:


# Remove batch dimension
actual_activations = actual_activations[0][0, :]


# In[19]:


# Print shape of the activation array
print(f"Activations of last convolutional layer have shape: {actual_activations.shape}")

# Print activation array
actual_activations


# Looks like everything worked out nicely! This is all for this lecture notebook (Grad-CAM Part 1). In Part 2 we will see how to calculate the gradients of the model's output with respect to the activations in this layer. This is the "Grad" part of Grad-CAM.

# **Congratulations on finishing this lecture notebook!** Hopefully you will now have a better understanding of how to leverage Keras's API power for computing activations in specific layers. Keep it up!
