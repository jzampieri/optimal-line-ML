import torch
import torch.nn as nn
import torch.nn.functional as F

class CarModel(nn.Module):
    def __init__(self):
        super(CarModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(5, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 3) 
        )

    def forward(self, x):
        return self.fc(x)
