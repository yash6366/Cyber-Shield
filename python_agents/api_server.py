from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from hunter_agent import HunterAgent
from classifier_agent import ClassifierAgent
from response_agent import ResponseAgent
import torch
import numpy as np
import logging
import os
from utils.logger import setup_logger
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = setup_logger('API_Server')
app = Flask(__name__)

# Configure CORS
CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[f"{os.getenv('RATE_LIMIT_PER_MINUTE', '60')}/minute"]
)

# Initialize agents
hunter_agent = HunterAgent()
classifier_agent = ClassifierAgent()
response_agent = ResponseAgent()

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({"error": str(e), "endpoint": f.__name__}), 500
    return wrapper

def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != os.getenv('API_KEY'):
            return jsonify({"error": "Invalid or missing API key"}), 401
        return f(*args, **kwargs)
    return wrapper

@app.before_request
def before_request():
    if not request.is_secure and os.getenv('FLASK_ENV') == 'production':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

@app.route('/health', methods=['GET'])
@limiter.limit("30/minute")
def health_check():
    return jsonify({
        "status": "healthy",
        "agents": {
            "hunter": "ready",
            "classifier": "ready",
            "response": "ready"
        }
    }), 200

@app.route('/metrics', methods=['GET'])
@limiter.limit("30/minute")
@require_api_key
def metrics():
    # Implement metrics collection
    return jsonify({"status": "ok"}), 200

@app.route('/hunter/train', methods=['POST'])
@limiter.limit("10/minute")
@require_api_key
def train_hunter():
    logger.info("Received request to train Hunter Agent")
    return jsonify({"status": "training started"}), 200

@app.route('/hunter/detect', methods=['POST'])
@limiter.limit("60/minute")
@require_api_key
@handle_errors
def detect_threat():
    data = request.json
    features = data.get('features')
    if not features:
        return jsonify({"error": "Missing features"}), 400
    input_tensor = torch.tensor([features], dtype=torch.float32)
    threat_detected = hunter_agent.detect_threat(input_tensor)
    return jsonify({
        "threat_detected": threat_detected,
        "confidence": float(threat_detected.item()) if hasattr(threat_detected, 'item') else float(threat_detected)
    }), 200

@app.route('/classifier/train', methods=['POST'])
@limiter.limit("10/minute")
@require_api_key
def train_classifier():
    logger.info("Received request to train Classifier Agent")
    classifier_agent.train()
    return jsonify({"status": "training started"}), 200

@app.route('/classifier/classify', methods=['POST'])
@limiter.limit("60/minute")
@require_api_key
@handle_errors
def classify_threat():
    data = request.json
    threat_description = data.get('threat_description')
    if not threat_description:
        return jsonify({"error": "Missing threat_description"}), 400
    label = classifier_agent.classify(threat_description)
    return jsonify({"label": label}), 200

@app.route('/response/train', methods=['POST'])
@limiter.limit("10/minute")
@require_api_key
def train_response():
    logger.info("Received request to train Response Agent")
    response_agent.train()
    return jsonify({"status": "training started"}), 200

@app.route('/response/execute', methods=['POST'])
@limiter.limit("60/minute")
@require_api_key
@handle_errors
def execute_response():
    data = request.json
    action = data.get('action')
    if not action:
        return jsonify({"error": "Missing action"}), 400
    success = response_agent.execute_response(action)
    return jsonify({"success": success}), 200

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
