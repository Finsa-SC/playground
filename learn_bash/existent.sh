#!/usr/bin/bash

if which uv &>/dev/null; then
  echo "Uv is installed"
else
  echo "Uv is not installed"
fi

if command -v zen-browser &>/dev/null; then
  echo "Zen browser installed"
else
  echo "Zen browser is not installed"
fi
