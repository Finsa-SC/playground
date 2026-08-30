#!/bin/bash

# Load environment variables from .env file
set -a
source /etc/user-activity-logger/.env
set +a

SERVICE_NAME="${SERVICE_NAME:-UserActivityLogger}"
LOG_LEVEL="${LOG_LEVEL:-INFO}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
BACKUP_DIR="${BACKUP_DIR:-/var/lib/user-activity-logger/backups}"

LOG_FILE="${LOG_DIR:-/var/log/user-activity-logger}/activity.log"

# Create directories if needed
mkdir -p "$(dirname "$LOG_FILE")" "$BACKUP_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$SERVICE_NAME] Starting with retention: ${RETENTION_DAYS} days" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Log Level: $LOG_LEVEL" >> "$LOG_FILE"

while true; do
  # Simulate logging user activity
  CURRENT_USERS=$(who | wc -l)
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$LOG_LEVEL] Currently active users: $CURRENT_USERS" >> "$LOG_FILE"
  
  # Cleanup old logs (simulated)
  EXPIRED_LOGS=$(find "$BACKUP_DIR" -mtime +$RETENTION_DAYS -type f 2>/dev/null | wc -l)
  if [ $EXPIRED_LOGS -gt 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cleaned up $EXPIRED_LOGS expired logs" >> "$LOG_FILE"
  fi
  
  sleep 15
done
