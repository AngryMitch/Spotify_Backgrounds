#!/bin/bash

# Script to create a virtual environment and activate it

# Define the name of the virtual environment directory
VENV_DIR=".venv"

# Function to activate the virtual environment
activate_venv() {
    if [ -f "$VENV_DIR/bin/activate" ]; then
        echo "Activating virtual environment..."
        source "$VENV_DIR/bin/activate"
    else
        echo "Virtual environment not found. Please create it first."
        exit 1
    fi
}

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating a new one..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        exit 1
    fi
fi

# Activate the virtual environment
activate_venv