#!/bin/bash

QUEUE_DIR="/var/lib/myworker/queue"
PROCESSED_DIR="/var/lib/myworker/processed"
LOG_FILE="/var/log/myworker.log"

# Create directories if not exist
mkdir -p "$QUEUE_DIR" "$PROCESSED_DIR"

while true; do
  # Look for files in queue directory
  for file in "$QUEUE_DIR"/*.task; do
    if [ -f "$file" ]; then
      # Process the task
      TASK_NAME=$(basename "$file")
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] Processing: $TASK_NAME" >> "$LOG_FILE"
      
      # Simulate work
      sleep 2
      
      # Move to processed
      mv "$file" "$PROCESSED_DIR/$TASK_NAME.done"
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] Completed: $TASK_NAME" >> "$LOG_FILE"
    fi
  done
  
  sleep 3
done
