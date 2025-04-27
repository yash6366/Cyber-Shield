# Dockerfile for Autonomous Cyber Defense Agents with Node.js and Python

# Use multi-stage build for smaller final image
FROM node:18-slim as node_base

WORKDIR /app

# Install Python, pip, curl and supervisor
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv curl supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment with correct permissions
RUN python3 -m venv /opt/venv && \
    chmod -R 755 /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy package.json and install Node dependencies
COPY frontend/package*.json frontend/
RUN cd frontend && npm install

# Copy rest of the application
COPY . .

# Build frontend
RUN cd frontend && npm run build

# Setup supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create log directory for supervisor
RUN mkdir -p /var/log/supervisor

# Expose ports for both services
EXPOSE 3000 5000

# Use supervisord as the entry point
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
