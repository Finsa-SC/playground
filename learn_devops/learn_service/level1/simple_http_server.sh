#!/bin/bash

PORT=8080
PID_FILE="/tmp/http_server.pid"

# Simple HTTP server using nc (netcat)
while true; do
  {
    echo -ne "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"
    echo "Service is up at $(date '+%Y-%m-%d %H:%M:%S')"
  } | nc -l -p $PORT -q 1
done
