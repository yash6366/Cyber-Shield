from http.server import BaseHTTPRequestHandler
from hunter_agent import HunterAgent
from classifier_agent import ClassifierAgent
from response_agent import ResponseAgent
import json
import torch
from flask import Flask, jsonify
from flask_cors import CORS
import os

# Initialize Flask for local development
app = Flask(__name__)
CORS(app)

# Initialize agents
hunter_agent = HunterAgent()
classifier_agent = ClassifierAgent()
response_agent = ResponseAgent()

class handler(BaseHTTPRequestHandler):
    def setup_response(self, status_code, content):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(content).encode())

    def do_OPTIONS(self):
        self.setup_response(200, {})

    def do_GET(self):
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

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == '/api/hunter/detect':
            try:
                features = data.get('features')
                if not features:
                    self.setup_response(400, {"error": "Missing features"})
                    return
                    
                input_tensor = torch.tensor([features], dtype=torch.float32)
                threat_detected = hunter_agent.detect_threat(input_tensor)
                
                response = {
                    "threat_detected": threat_detected,
                    "confidence": float(threat_detected.item()) if hasattr(threat_detected, 'item') else float(threat_detected)
                }
                self.setup_response(200, response)
            except Exception as e:
                self.setup_response(500, {"error": str(e)})
            return

        elif self.path == '/api/classifier/classify':
            try:
                threat_description = data.get('threat_description')
                if not threat_description:
                    self.setup_response(400, {"error": "Missing threat description"})
                    return
                    
                label = classifier_agent.classify(threat_description)
                self.setup_response(200, {"label": label})
            except Exception as e:
                self.setup_response(500, {"error": str(e)})
            return

        elif self.path == '/api/response/execute':
            try:
                action = data.get('action')
                if not action:
                    self.setup_response(400, {"error": "Missing action"})
                    return
                    
                success = response_agent.execute_response(action)
                self.setup_response(200, {"success": success})
            except Exception as e:
                self.setup_response(500, {"error": str(e)})
            return

# For local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)