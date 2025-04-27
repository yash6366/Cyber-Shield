from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Add python_agents directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from python_agents.hunter_agent import HunterAgent
from python_agents.classifier_agent import ClassifierAgent
from python_agents.response_agent import ResponseAgent

# Initialize agents (only once, outside the handler)
hunter_agent = HunterAgent()
classifier_agent = ClassifierAgent()
response_agent = ResponseAgent()

def validate_api_key(headers):
    api_key = headers.get('X-API-Key')
    expected_key = os.environ.get('API_KEY')
    return api_key == expected_key

def get_clean_path(path):
    """Remove /api prefix and trailing slashes from path"""
    path = path.rstrip('/')
    if path.startswith('/api/'):
        path = path[4:]  # Remove /api prefix
    return path

class handler(BaseHTTPRequestHandler):
    def setup_response(self, status_code, content):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-API-Key')
        self.end_headers()
        self.wfile.write(json.dumps(content).encode())

    def do_OPTIONS(self):
        self.setup_response(200, {})

    def do_GET(self):
        if not validate_api_key(self.headers):
            self.setup_response(401, {"error": "Invalid API key"})
            return

        clean_path = get_clean_path(self.path)
        if clean_path == 'health':
            content = {
                "status": "healthy",
                "agents": {
                    "hunter": "ready",
                    "classifier": "ready",
                    "response": "ready"
                }
            }
            self.setup_response(200, content)
            return
        
        self.setup_response(404, {"error": "Not found"})

    def do_POST(self):
        if not validate_api_key(self.headers):
            self.setup_response(401, {"error": "Invalid API key"})
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        try:
            clean_path = get_clean_path(self.path)
            
            if clean_path == 'hunter/detect':
                features = data.get('features')
                if not features:
                    self.setup_response(400, {"error": "Missing features"})
                    return
                    
                threat_detected = hunter_agent.detect_threat(features)
                response = {
                    "threat_detected": threat_detected,
                    "confidence": float(threat_detected) if isinstance(threat_detected, (int, float)) else None
                }
                self.setup_response(200, response)
                return

            elif clean_path == 'classifier/classify':
                threat_description = data.get('threat_description')
                if not threat_description:
                    self.setup_response(400, {"error": "Missing threat description"})
                    return
                    
                result = classifier_agent.classify(threat_description)
                self.setup_response(200, result)
                return

            elif clean_path == 'response/execute':
                action = data.get('action')
                if not action:
                    self.setup_response(400, {"error": "Missing action"})
                    return
                    
                success = response_agent.execute_response(action)
                self.setup_response(200, {"success": success})
                return
            
            self.setup_response(404, {"error": "Not found"})

        except Exception as e:
            self.setup_response(500, {"error": str(e)})