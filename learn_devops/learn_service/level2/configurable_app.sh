#!/bin/bash

# Load environment variables from .env file
set -a
source /etc/configurable_app/.env
set +a

APP_NAME="${APP_NAME:-MyApp}"
APP_PORT="${APP_PORT:-3000}"
LOG_LEVEL="${LOG_LEVEL:-INFO}"
MAX_WORKERS="${MAX_WORKERS:-4}"

LOG_FILE="${LOG_DIR:-/var/log/configurable_app}/application.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$APP_NAME] Starting on port $APP_PORT (Workers: $MAX_WORKERS)" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Log Level: $LOG_LEVEL" >> "$LOG_FILE"

while true; do
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$LOG_LEVEL] App running..." >> "$LOG_FILE"
  sleep 10
done
