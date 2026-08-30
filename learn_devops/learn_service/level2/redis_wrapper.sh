#!/bin/bash

set -a
source /etc/cache-service/.env
set +a

REDIS_PORT="${REDIS_PORT:-6379}"
REDIS_BIND="${REDIS_BIND:-127.0.0.1}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Redis on $REDIS_BIND:$REDIS_PORT"

# Run actual redis-server
redis-server --port $REDIS_PORT --bind $REDIS_BIND --loglevel ${REDIS_LOG_LEVEL:-notice}
