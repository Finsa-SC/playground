#!/usr/bin/env python3

import os
import sys
import signal
import logging
from flask import Flask, jsonify
import redis
from dotenv import load_dotenv
import time

# Load .env
load_dotenv('/etc/api-gateway/.env')

app = Flask(__name__)

# Config
API_PORT = int(os.getenv('API_PORT', 5000))
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_RETRY_MAX = int(os.getenv('REDIS_RETRY_MAX', 5))
SERVICE_NAME = os.getenv('SERVICE_NAME', 'APIGateway')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(SERVICE_NAME)

# Global redis client
redis_client = None

def connect_redis():
    """Connect to Redis with retry logic"""
    global redis_client
    retry_count = 0
    
    while retry_count < REDIS_RETRY_MAX:
        try:
            logger.info(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}")
            redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                socket_connect_timeout=5,
                decode_responses=True
            )
            redis_client.ping()
            logger.info("Successfully connected to Redis")
            return True
        except Exception as e:
            retry_count += 1
            logger.warning(f"Redis connection failed (attempt {retry_count}/{REDIS_RETRY_MAX}): {e}")
            if retry_count < REDIS_RETRY_MAX:
                time.sleep(2)
    
    logger.error("Failed to connect to Redis after retries")
    return False

def signal_handler(signum, frame):
    """Graceful shutdown"""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': SERVICE_NAME
    }), 200

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint with Redis connection check"""
    redis_status = 'connected'
    try:
        if redis_client:
            redis_client.ping()
        else:
            redis_status = 'disconnected'
    except Exception as e:
        redis_status = f'error: {str(e)}'
    
    return jsonify({
        'service': SERVICE_NAME,
        'status': 'running',
        'redis': redis_status
    }), 200

if __name__ == '__main__':
    logger.info(f"Starting {SERVICE_NAME} on port {API_PORT}")
    
    # Setup signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Connect to Redis
    if not connect_redis():
        logger.error("Cannot start without Redis connection")
        sys.exit(1)
    
    # Start Flask
    app.run(host='0.0.0.0', port=API_PORT, debug=False)
