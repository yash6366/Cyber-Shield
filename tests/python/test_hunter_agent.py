import pytest
import torch
import numpy as np
from python_agents.hunter_agent import HunterAgent, HunterAgentModel

@pytest.fixture
def hunter_agent():
    return HunterAgent()

def test_hunter_agent_initialization(hunter_agent):
    assert isinstance(hunter_agent.model, HunterAgentModel)
    assert isinstance(hunter_agent.criterion, torch.nn.CrossEntropyLoss)
    assert isinstance(hunter_agent.optimizer, torch.optim.Adam)

def test_detect_threat(hunter_agent):
    # Create mock input tensor
    input_tensor = torch.randn(1, 100)
    result = hunter_agent.detect_threat(input_tensor)
    assert isinstance(result, bool)

def test_model_forward_pass():
    model = HunterAgentModel(input_size=100, hidden_size=50, output_size=2)
    x = torch.randn(1, 100)
    output = model(x)
    assert output.shape == (1, 2)
    assert torch.allclose(torch.sum(output), torch.tensor(1.0))  # Softmax output sums to 1