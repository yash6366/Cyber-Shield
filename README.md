# CyberShield - Autonomous Cyber Defense System

> An AI-powered cybersecurity defense system using multi-agent architecture for real-time threat detection and response.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18.x-green.svg)](https://nodejs.org/)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Environment Variables](#environment-variables)
- [Production Deployment](#production-deployment)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview
CyberShield is an advanced cybersecurity defense system that leverages AI agents to detect, classify, and respond to threats in real-time. The system uses a multi-agent architecture with specialized components for threat hunting, classification, and automated response.

## Features
- 🔍 **Real-time Threat Detection**: ML-powered detection of anomalous network behavior
- 🤖 **AI-driven Classification**: LLM-based threat classification with RAG
- ⚡ **Automated Response**: Configurable policy-based threat response
- 📊 **Interactive Dashboard**: Real-time visualization of system state
- 🔄 **Simulation Environment**: Built-in attack simulation for testing
- 🚀 **Scalable Architecture**: Microservices-based design with Docker support

## Prerequisites
- Python 3.11 or higher
- Node.js 18.x or higher
- Docker & Docker Compose
- Git
- 8GB RAM minimum (16GB recommended)
- 20GB disk space

## Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/cybershield.git
cd cybershield

# Start with Docker Compose
docker compose up -d

# Access the dashboard
open http://localhost:3000
```

## Detailed Setup

### Development Environment
1. Create Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
npm run build
cd ..
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Start development servers:
```bash
# Terminal 1 - API Server
python python_agents/api_server.py

# Terminal 2 - Frontend
cd frontend && npm start
```

### Production Environment
1. Update environment variables in `.env`
2. Build and start containers:
```bash
docker compose -f docker-compose.prod.yml up -d
```

## Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| NODE_ENV | Environment mode | development |
| API_PORT | Backend API port | 5000 |
| FRONTEND_PORT | Frontend server port | 3000 |
| LOG_LEVEL | Logging verbosity | info |
| FLASK_ENV | Flask environment | development |
| DB_HOST | Database host | localhost |
| REDIS_URL | Redis connection URL | redis://localhost |

## Production Deployment

### System Requirements
- 16GB RAM minimum
- 4 CPU cores minimum
- 50GB SSD storage
- Ubuntu 20.04 or higher

### Security Considerations
1. Enable HTTPS
2. Configure firewall rules
3. Set up monitoring
4. Enable regular backups
5. Implement access control

### Deployment Steps
1. Configure SSL certificates
2. Set up reverse proxy (nginx recommended)
3. Configure environment variables
4. Deploy with Docker Compose
5. Set up monitoring and alerts

## API Documentation
API documentation is available at `/api/docs` when running the server.
See [API.md](docs/API.md) for detailed endpoint documentation.

## Testing
```bash
# Run Python tests
pytest

# Run JavaScript tests
cd frontend && npm test

# Integration tests
python tests/integration/run_tests.py
```

## Monitoring
- Health check endpoint: `/api/health`
- Metrics endpoint: `/api/metrics`
- Prometheus integration available
- Grafana dashboards in `monitoring/dashboards/`

## Troubleshooting

### Common Issues
1. **Services not starting**
   - Check logs: `docker compose logs`
   - Verify ports not in use
   - Check environment variables

2. **Performance issues**
   - Check system resources
   - Verify Redis connection
   - Check log levels

3. **API errors**
   - Verify API server running
   - Check network connectivity
   - Validate request format

### Logs
- API logs: `/var/log/api_server.log`
- Frontend logs: `/var/log/frontend.log`
- Agent logs: `/var/log/agents/*.log`

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License
This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Support
- Documentation: [docs/](docs/)
- Issues: GitHub Issues
- Community: [Discord](https://discord.gg/cybershield)# Cyber-Shield
# Cyber-Shield
