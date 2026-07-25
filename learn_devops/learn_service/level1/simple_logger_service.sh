#!/bin/bash

# Simple logger service
LOG_FILE="/tmp/myservice.log"

while true; do
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Service is running..." >> $LOG_FILE
  sleep 5
done