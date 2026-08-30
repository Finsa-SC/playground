#!/bin/bash

TMP=$(mktemp -d)
cleanup() {
    echo "Cleaning up resource..."
    rm -rf "$TMP"
}

trap cleanup EXIT 

store_tmp() {
    mkdir -p "$TMP/"{bin,env,lib,app}
}

echo "Starting process..."
store_tmp
read  
echo "Stopping process..."

