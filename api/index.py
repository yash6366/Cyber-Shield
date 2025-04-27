from http.server import BaseHTTPRequestHandler
import json
import os
from hunter_agent import HunterAgent
from classifier_agent import ClassifierAgent
from response_agent import ResponseAgent

# Initialize agents (only once, outside the handler)
hunter_agent = HunterAgent()
classifier_agent = ClassifierAgent()
response_agent = ResponseAgent()

def validate_api_key(headers):
    api_key = headers.get('X-API-Key')
    expected_key = os.environ.get('API_KEY')
    return api_key == expected_key

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

        if self.path == '/api/health':
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
            if self.path == '/api/hunter/detect':
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

            elif self.path == '/api/classifier/classify':
                threat_description = data.get('threat_description')
                if not threat_description:
                    self.setup_response(400, {"error": "Missing threat description"})
                    return
                    
                label = classifier_agent.classify(threat_description)
                self.setup_response(200, {"label": label})
                return

            elif self.path == '/api/response/execute':
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