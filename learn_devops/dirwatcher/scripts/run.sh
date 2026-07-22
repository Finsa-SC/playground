#!/usr/bin/env bash
# Convenience wrapper for running the watcher locally.
set -e

export $(grep -v '^#' .env | xargs)

python -m dirwatcher.main
