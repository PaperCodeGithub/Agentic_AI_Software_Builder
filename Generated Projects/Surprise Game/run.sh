#!/usr/bin/env bash

# One‑click script to set up a virtual environment, install dependencies, and launch Quantum Maze

# Exit on any error
set -e

# Directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Create virtual environment in .venv inside the script directory
VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements.txt"

# Run the game
python "$SCRIPT_DIR/src/main.py"
