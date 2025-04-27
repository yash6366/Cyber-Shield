import torch
import torch.nn as nn
import torch.optim as optim
import logging
from utils.logger import setup_logger
from utils.model_manager import ModelManager

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
        self.model_manager = ModelManager()
        self.model = self._load_or_init_model()
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        logger.info("HunterAgent initialized with model.")

    def _load_or_init_model(self):
        try:
            # Try to load the latest model
            model_data = self.model_manager.load_model("hunter", "latest")
            model = HunterAgentModel(
                **model_data["hyperparameters"]
            )
            model.load_state_dict(model_data["state_dict"])
            logger.info(f"Loaded model with metrics: {model_data['metadata']['metrics']}")
        except (ValueError, FileNotFoundError):
            # Initialize new model if none exists
            model = HunterAgentModel()
            logger.info("Initialized new model")
        return model

    def train(self, data_loader, epochs=5):
        self.model.train()
        metrics = {"epoch_losses": []}
        
        for epoch in range(epochs):
            total_loss = 0
            correct = 0
            total = 0
            
            for inputs, labels in data_loader:
                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
                
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
            
            epoch_loss = total_loss / len(data_loader)
            accuracy = correct / total
            metrics["epoch_losses"].append(epoch_loss)
            logger.info(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss:.4f}, Accuracy: {accuracy:.4f}")

        # Save model with metrics
        metrics.update({
            "final_loss": metrics["epoch_losses"][-1],
            "final_accuracy": accuracy
        })
        
        self.model_manager.save_model(
            model=self.model,
            model_type="hunter",
            version=f"{epochs}.0",
            metrics=metrics,
            hyperparameters={
                "input_size": 100,
                "hidden_size": 50,
                "output_size": 2
            }
        )
        logger.info("Training complete.")

    def detect_threat(self, input_tensor):
        self.model.eval()
        with torch.no_grad():
            output = self.model(input_tensor)
            _, predicted = torch.max(output, 1)
            confidence = output[0][predicted.item()].item()
            threat_detected = predicted.item() == 1
            logger.info(f"Threat detection result: {threat_detected} (confidence: {confidence:.2f})")
            return threat_detected

if __name__ == "__main__":
    logger.info("HunterAgent module run directly - add training and detection logic here.")
