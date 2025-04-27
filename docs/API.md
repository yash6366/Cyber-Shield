# CyberShield API Documentation

## Overview
This document describes the REST API endpoints for the CyberShield autonomous cyber defense system.

## Base URL
- Development: `http://localhost:5000/api`
- Production: `https://your-domain.com/api`

## Authentication
All API endpoints require authentication using an API key. Include the key in the request header:
```
X-API-Key: your-api-key-here
```

## Endpoints

### Health Check
GET `/health`

Check the health status of all system components.

**Response**
```json
{
    "status": "healthy",
    "agents": {
        "hunter": "ready",
        "classifier": "ready",
        "response": "ready"
    }
}
```

### Threat Detection
POST `/hunter/detect`

Detect threats in network traffic or system logs.

**Request Body**
```json
{
    "features": [0.1, 0.2, ..., 0.9]  // 100-dimensional feature vector
}
```

**Response**
```json
{
    "threat_detected": true,
    "confidence": 0.95
}
```

### Threat Classification
POST `/classifier/classify`

Classify detected threats using LLM-based analysis.

**Request Body**
```json
{
    "threat_description": "Suspicious traffic detected from IP 192.168.1.100"
}
```

**Response**
```json
{
    "label": "Brute Force Attack",
    "confidence": 0.85,
    "details": {
        "severity": "High",
        "technique": "T1110",
        "tactics": ["Initial Access", "Credential Access"]
    }
}
```

### Response Execution
POST `/response/execute`

Execute automated response actions.

**Request Body**
```json
{
    "action": {
        "type": "block_ip",
        "target": "192.168.1.100",
        "duration": 3600
    }
}
```

**Response**
```json
{
    "success": true,
    "action_id": "resp_123xyz",
    "timestamp": "2025-04-27T10:30:15Z"
}
```

### Metrics
GET `/metrics`

Get system performance metrics.

**Response**
```json
{
    "status": "ok",
    "metrics": {
        "threats_detected": 150,
        "false_positives": 3,
        "response_time_ms": 245,
        "model_accuracy": 0.98
    }
}
```

## Rate Limiting
- Standard rate limits: 60 requests per minute
- Training endpoints: 10 requests per minute
- Health check: 30 requests per minute

## Error Responses
All endpoints may return the following error responses:

### 401 Unauthorized
```json
{
    "error": "Invalid or missing API key"
}
```

### 400 Bad Request
```json
{
    "error": "Missing required field: features"
}
```

### 429 Too Many Requests
```json
{
    "error": "Rate limit exceeded",
    "retry_after": 30
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error",
    "request_id": "req_abc123"
}
```