# -*- coding: utf-8 -*-
"""Poojitha_Venkatram_HW2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lfnpJSx8Fg3JrhC6RVw2zRn0F_4_cA3s

#### DATA 255 Homework-2

#### Poojitha Venkatram

#### Github Link- https://github.com/poojithavenkatram/Deep-Learning
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

# Defining the transformation
transform = ToTensor()

# Defining the QMNIST datasets
qmnist_trainset = datasets.QMNIST(root='data', train=True, download=True, transform=transform)
qmnist_testset = datasets.QMNIST(root='data', train=False, download=True, transform=transform)


print(len(qmnist_trainset))  # Number of samples in the QMNIST training set
print(len(qmnist_testset))   # Number of samples in the QMNIST test set

print(qmnist_trainset.data.size())   # Size of the training data
print(qmnist_trainset.targets.size())   # Size of the training labels

print(qmnist_testset.data.size())    # Size of the test data
print(qmnist_testset.targets.size())    # Size of the test labels

"""#### Visualization of the QMNIST Dataset"""

# Define a function to visualize QMNIST samples
def visualize_qmnist_samples(qmnist_dataset, cols=5, rows=5):
    figure = plt.figure(figsize=(10, 8))

    for i in range(1, cols * rows + 1):
        sample_idx = torch.randint(len(qmnist_dataset), size=(1,)).item()
        img, label = qmnist_dataset[sample_idx]
        figure.add_subplot(rows, cols, i)
        plt.title(label)
        plt.axis("off")
        plt.imshow(img.squeeze(), cmap="gray")

    plt.show()

# Visualize some samples from the QMNIST training set
visualize_qmnist_samples(qmnist_trainset)

# Visualize some samples from the QMNIST test set
visualize_qmnist_samples(qmnist_testset)

# Print the number of samples in the QMNIST training and test sets
print(len(qmnist_trainset))  # Number of samples in the QMNIST training set
print(len(qmnist_testset))   # Number of samples in the QMNIST test set

# Create data loaders
train_loader = DataLoader(qmnist_trainset, batch_size=64, shuffle=True)
test_loader = DataLoader(qmnist_testset, batch_size=64, shuffle=False)

"""#### Define functions to train the model and evaluate results"""

import torch
import torch.nn as nn

class QMNIST(nn.Module):
    def __init__(self):
        super(QMNIST, self).__init__()
        # Defining the first fully connected layer with 128 neurons
        self.fc1 = nn.Linear(28 * 28, 128)
        # Defining the second fully connected layer with 64 neurons
        self.fc2 = nn.Linear(128, 64)
        # Defining the output layer with 10 neurons for classification
        self.fc3 = nn.Linear(64, 10)

    def forward(self, x):
        # Flattening the input tensor
        x = x.view(-1, 28 * 28)
        # Passing through the first fully connected layer and apply ReLU activation
        x = torch.relu(self.fc1(x))
        # Passing through the second fully connected layer and apply ReLU activation
        x = torch.relu(self.fc2(x))
        # Passing through the output layer (no activation applied)
        x = self.fc3(x)
        return x

# Initializing the neural network
model = QMNIST()

"""### Training the Model"""

# Defining the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training the neural network
num_epochs = 5
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        if i % 100 == 99:  # print every 100 mini-batches
            print(f'Epoch {epoch + 1}, Batch {i + 1}, Loss: {running_loss / 100}')
            running_loss = 0.0

print('Finished Training')

"""#### Evaluate the model prediction accuracy on the train and test datasets"""

def evaluate(model, dataloader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for data in dataloader:
            images, labels = data
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = correct / total
    return accuracy

# Evaluate on train dataset
train_accuracy = evaluate(model, train_loader)
print('Accuracy on train set: {:.2f}%'.format(train_accuracy * 100))

# Evaluate on test dataset
test_accuracy = evaluate(model, test_loader)
print('Accuracy on test set: {:.2f}%'.format(test_accuracy * 100))

"""### Adding another dense layer of 128 nodes to the architecture will likely increase the model's capacity to capture more complex patterns in the data. This additional layer would introduce more parameters and non-linearity to the model, thus enabling it to learn more intricate features from the input images."""

import torch
import torch.nn as nn

class QMNIST(nn.Module):
    def __init__(self):
        super(QMNIST, self).__init__()
        # Define the first fully connected layer with 128 neurons
        self.fc1 = nn.Linear(28 * 28, 128)
        # Define the second fully connected layer with 128 neurons
        self.fc2 = nn.Linear(128, 128)  # New layer
        # Define the third fully connected layer with 64 neurons
        self.fc3 = nn.Linear(128, 64)
        # Define the output layer with 10 neurons for classification
        self.fc4 = nn.Linear(64, 10)

    def forward(self, x):
        # Flatten the input tensor
        x = x.view(-1, 28 * 28)
        # Pass through the first fully connected layer and apply ReLU activation
        x = torch.relu(self.fc1(x))
        # Pass through the second fully connected layer and apply ReLU activation
        x = torch.relu(self.fc2(x))
        # Pass through the third fully connected layer and apply ReLU activation
        x = torch.relu(self.fc3(x))
        # Pass through the output layer (no activation applied)
        x = self.fc4(x)
        return x

# Initialize the neural network
model = QMNIST()

# Defining the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training the neural network
num_epochs = 5
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        if i % 100 == 99:  # print every 100 mini-batches
            print(f'Epoch {epoch + 1}, Batch {i + 1}, Loss: {running_loss / 100}')
            running_loss = 0.0

print('Finished Training')

# Evaluating the model
model.eval()
predictions = []
correct = 0
total = 0
with torch.no_grad():
    for data in test_loader:
        images, labels = data
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        predictions.extend(predicted.numpy())  # Store predictions
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f'Accuracy on test set: { correct / total}%')

"""### The results of the modified model are as follows,


*   Adding another dense layer of 128 nodes enhanced the model's capacity to learn complex patterns and representations from the data.
*   The increase in accuracy from 97.20% to 97.26% suggests that the additional layer contributed positively to the model's performance.
*   This improvement implies better feature extraction, reduced overfitting, and dataset-specific benefits, leading to a slight enhancement in accuracy on the test set.

### Experimenting with different Hyperparameters
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Defining the neural network architecture
class QMNIST(nn.Module):
    def __init__(self, dropout_rate=0.0, activation_fn=torch.relu):
        super(QMNIST, self).__init__()
        # Define the first fully connected layer with 128 neurons
        self.fc1 = nn.Linear(28 * 28, 128)
        # Define the second fully connected layer with 128 neurons
        self.fc2 = nn.Linear(128, 128)  # New layer
        # Define the third fully connected layer with 64 neurons
        self.fc3 = nn.Linear(128, 64)
        # Define the output layer with 10 neurons for classification
        self.fc4 = nn.Linear(64, 10)
        # Define dropout layer
        self.dropout = nn.Dropout(dropout_rate)
        # Define activation function
        self.activation_fn = activation_fn

    def forward(self, x):
        # Flatten the input tensor
        x = x.view(-1, 28 * 28)
        # Pass through the first fully connected layer and apply activation and dropout
        x = self.activation_fn(self.fc1(x))
        x = self.dropout(x)
        # Pass through the second fully connected layer and apply activation and dropout
        x = self.activation_fn(self.fc2(x))
        x = self.dropout(x)
        # Pass through the third fully connected layer and apply activation and dropout
        x = self.activation_fn(self.fc3(x))
        x = self.dropout(x)
        # Pass through the output layer (no activation applied)
        x = self.fc4(x)
        return x

# Defining the function to train the model
def train(model, train_loader, optimizer, criterion):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    return running_loss / len(train_loader)

# Defining function to evaluate the model
def evaluate(model, test_loader, criterion):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    return correct / total

# Defining hyperparameters
learning_rate = 0.001
dropout_rate = 0.2
activation_fn = torch.relu

# Initializing the model
model = QMNIST(dropout_rate=dropout_rate, activation_fn=activation_fn)

# Defining the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training the model
num_epochs = 10
for epoch in range(num_epochs):
    train_loss = train(model, train_loader, optimizer, criterion)
    test_accuracy = evaluate(model, test_loader, criterion)
    print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss:.4f}, Test Accuracy: {test_accuracy:.4f}")

print('Finished Training')

# Printing the model performance
print(f"Test Accuracy: {test_accuracy:.4f}")

"""##### The output indicates the performance of the neural network model on the test data after training for 10 epochs with the specified hyperparameters. Here's the breakdown:
- The training loss decreases gradually over epochs, indicating that the model is learning and improving its fit to the training data.
- The test accuracy increases over epochs, reaching 97.69% after 10 epochs. This indicates that the model is generalizing well to unseen data and performing better with the specified hyperparameters compared to previous epochs.

Overall, the change in hyperparameters has led to improvements in the model's performance, as evidenced by the decreasing loss and increasing accuracy on the test dataset.

### Prediction on Test Set
"""

import matplotlib.pyplot as plt

def visualize_image_and_predictions(image, label, predicted_label, predictions, qmnist_testset):

    # Display some predictions on test data
    fig, axes = plt.subplots(ncols=10, sharex=False,
                             sharey=True, figsize=(20, 4))
    for i in range(10):
        axes[i].set_title(predictions[i])
        img, lbl = qmnist_testset[i]
        axes[i].imshow(img.squeeze(), cmap='gray')
        axes[i].get_xaxis().set_visible(False)
        axes[i].get_yaxis().set_visible(False)
    plt.show()

# Example
visualize_image_and_predictions(image_numpy, label.item(), predictions[1], predictions, qmnist_testset)

"""# Thus, the model makes correct predictions on the test data above."""