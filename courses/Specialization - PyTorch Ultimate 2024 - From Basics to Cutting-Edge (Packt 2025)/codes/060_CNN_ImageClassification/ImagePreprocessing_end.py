#%%
import torch
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
# %% import image
img = Image.open('060_CNN_ImageClassification/kiki.jpg')
img

# %% compose a series of steps
preprocess_steps = transforms.Compose([
    transforms.Resize(300),  # better (300, 300)
    transforms.RandomRotation(50),
    transforms.CenterCrop(500),
    #transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),  # ImageNet values
    transforms.Grayscale(),
    transforms.RandomVerticalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5), (0.5)),  # ImageNet values
])
x = preprocess_steps(img)
plt.imshow(x.squeeze(), cmap='gray')
plt.show()

# %% get the mean and std of given image
print(x.mean([1, 2]), x.std([1, 2]))