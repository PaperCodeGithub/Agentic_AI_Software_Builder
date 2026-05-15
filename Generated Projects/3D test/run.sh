#!/usr/bin/env bash

# Exit immediately if a command exits with a non‑zero status.
set -e

echo "Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Launching the game..."
python3 main.py
