#!/bin/bash

LOG_ARCHIVE_DIR="/var/lib/logrotator/archive"
ACTIVE_LOG="/var/lib/logrotator/app.log"
MAX_LOG_SIZE=1048576  # 1MB

while true; do
  # Check if log file exists and size
  if [ -f "$ACTIVE_LOG" ]; then
    CURRENT_SIZE=$(stat -f%z "$ACTIVE_LOG" 2>/dev/null || stat -c%s "$ACTIVE_LOG" 2>/dev/null)
    
    if [ "$CURRENT_SIZE" -gt "$MAX_LOG_SIZE" ]; then
      # Rotate: move current log to archive with timestamp
      TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
      mv "$ACTIVE_LOG" "$LOG_ARCHIVE_DIR/app_$TIMESTAMP.log.old"
      
      # Create new empty log file
      touch "$ACTIVE_LOG"
      
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] Log rotated: app_$TIMESTAMP.log.old" >> "$ACTIVE_LOG"
    fi
  fi
  
  sleep 5
done
