import pytest
import torch
import torch.nn as nn
import os
import shutil
from utils.model_manager import ModelManager

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 2)
    
    def forward(self, x):
        return self.fc(x)

@pytest.fixture
def model_manager():
    test_path = "test_models"
    manager = ModelManager(test_path)
    yield manager
    # Cleanup after tests
    if os.path.exists(test_path):
        shutil.rmtree(test_path)

@pytest.fixture
def sample_model():
    return SimpleModel()

def test_model_save_load(model_manager, sample_model):
    metrics = {"accuracy": 0.95, "loss": 0.1}
    hyperparameters = {"lr": 0.001, "batch_size": 32}
    
    # Save model
    model_id = model_manager.save_model(
        sample_model, "test", "1.0", metrics, hyperparameters
    )
    
    # Load model
    loaded = model_manager.load_model("test", "1.0")
    
    assert loaded["metadata"]["metrics"] == metrics
    assert loaded["hyperparameters"] == hyperparameters
    
    # Load state dict into a new model
    new_model = SimpleModel()
    new_model.load_state_dict(loaded["state_dict"])
    
    # Verify model parameters are the same
    for p1, p2 in zip(sample_model.parameters(), new_model.parameters()):
        assert torch.equal(p1, p2)

def test_latest_version(model_manager, sample_model):
    # Save multiple versions
    metrics = {"accuracy": 0.9}
    model_manager.save_model(sample_model, "test", "1.0", metrics)
    model_manager.save_model(sample_model, "test", "2.0", metrics)
    
    # Load latest should get version 2.0
    loaded = model_manager.load_model("test", "latest")
    assert loaded["metadata"]["version"] == "2.0"

def test_archive_model(model_manager, sample_model):
    metrics = {"accuracy": 0.9}
    model_manager.save_model(sample_model, "test", "1.0", metrics)
    
    # Archive the model
    model_manager.archive_model("test", "1.0")
    
    # Verify model is marked as archived
    model_id = "test_v1.0"
    assert model_manager.metadata["models"][model_id]["archived"] == True
    assert "archive_date" in model_manager.metadata["models"][model_id]

def test_get_model_metrics(model_manager, sample_model):
    metrics = {"accuracy": 0.95, "loss": 0.1}
    model_manager.save_model(sample_model, "test", "1.0", metrics)
    
    loaded_metrics = model_manager.get_model_metrics("test", "1.0")
    assert loaded_metrics == metrics