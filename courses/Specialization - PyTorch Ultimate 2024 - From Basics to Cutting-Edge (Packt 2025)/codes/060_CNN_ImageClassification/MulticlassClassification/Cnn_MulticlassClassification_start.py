#%% packages
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
os.getcwd()

# %% transform and load data
# TODO: set up image transforms
transform = transforms.Compose(
    [transforms.Resize((50,50)), #((64,64)), #(32,32)),
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    transforms.Normalize((0.5, ), (0.5, ))])

# TODO: set up train and test datasets
batch_size = 4
trainset = torchvision.datasets.ImageFolder(root='060_CNN_ImageClassification/MulticlassClassification/train', transform=transform)
testset = torchvision.datasets.ImageFolder(root='060_CNN_ImageClassification/MulticlassClassification/test', transform=transform)

# TODO: set up data loaders
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=True)

# %%
CLASSES = ['affenpinscher', 'akita', 'corgi']
NUM_CLASSES = len(CLASSES)

# TODO: set up model class
class ImageMulticlassClassificationNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 3) # BS, 6, 62, 62
        self.pool = nn.MaxPool2d(2, 2) # BS, 6, 31, 31
        self.conv2 = nn.Conv2d(6, 16, 3) # BS, 16, 29, 29 # BS, 16, 14, 14
        self.fc1 = nn.Linear(16 * 11 * 11, 128)  #(16 * 6 * 6, 128) 
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, NUM_CLASSES)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax()


    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.softmax(x)
        return x

# input = torch.rand(1, 1, 50, 50) # BS, C, H, W
model = ImageMulticlassClassificationNet()      
#print(model(input).shape)

# %% loss function and optimizer
# TODO: set up loss function and optimizer
loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters())
# %% training
NUM_EPOCHS = 10
for epoch in range(NUM_EPOCHS):
    for i, data in enumerate(trainloader, 0):
        inputs, labels = data
        # TODO: define training loop
        #print(labels.shape)
        optimizer.zero_grad()
        preds = model(inputs)
        loss = loss_fn(preds, labels) # order is important
        loss.backward()
        optimizer.step()

    print(f'Epoch {epoch}/{NUM_EPOCHS}, Loss: {loss.item():.4f}')


# %% test
y_test = []
y_test_hat = []
for i, data in enumerate(testloader, 0):
    inputs, y_test_temp = data
    with torch.no_grad():
        y_test_hat_temp = model(inputs).round()
    
    y_test.extend(y_test_temp.numpy())
    y_test_hat.extend(y_test_hat_temp.numpy())

# %%
acc = accuracy_score(y_test, np.argmax(y_test_hat, axis=1))
print(f'Accuracy: {acc*100:.2f} %')
# %% confusion matrix
print(confusion_matrix(y_test, np.argmax(y_test_hat, axis=1)))
# %%
