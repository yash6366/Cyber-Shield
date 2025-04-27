import torch
import torch.nn as nn
import torch.optim as optim
import logging
from utils.logger import setup_logger

logger = setup_logger('HunterAgent')

class HunterAgentModel(nn.Module):
    def __init__(self, input_size=100, hidden_size=50, output_size=2):
        super(HunterAgentModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out

class HunterAgent:
    def __init__(self):
        self.model = HunterAgentModel()
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        logger.info("HunterAgent initialized with model.")

    def train(self, data_loader, epochs=5):
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            for inputs, labels in data_loader:
                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            logger.info(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}")
        logger.info("Training complete.")

    def detect_threat(self, input_tensor):
        self.model.eval()
        with torch.no_grad():
            output = self.model(input_tensor)
            _, predicted = torch.max(output, 1)
            threat_detected = predicted.item() == 1
            logger.info(f"Threat detection result: {threat_detected}")
            return threat_detected

if __name__ == "__main__":
    logger.info("HunterAgent module run directly - add training and detection logic here.")
