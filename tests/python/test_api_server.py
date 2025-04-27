import pytest
import json
from python_agents.api_server import app
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert all(agent == 'ready' for agent in data['agents'].values())

@pytest.mark.parametrize('endpoint', [
    '/hunter/detect',
    '/classifier/classify',
    '/response/execute'
])
def test_api_key_required(client, endpoint):
    response = client.post(endpoint)
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'Invalid or missing API key' in data['error']

def test_detect_threat(client):
    headers = {'X-API-Key': os.getenv('API_KEY', 'test-key')}
    features = [0.0] * 100
    response = client.post('/hunter/detect', 
                         json={'features': features},
                         headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'threat_detected' in data
    assert isinstance(data['threat_detected'], bool)

def test_classify_threat(client):
    headers = {'X-API-Key': os.getenv('API_KEY', 'test-key')}
    description = "Suspicious activity detected"
    response = client.post('/classifier/classify',
                         json={'threat_description': description},
                         headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'label' in data