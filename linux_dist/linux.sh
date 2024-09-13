#!/bin/bash

# Script to install requirements

# Check if requirements.txt file exists
if [ ! -f requirements.txt ]; then
    echo "requirements.txt not found! Make sure this script is run in the project directory."
    exit 1
fi

# Install the requirements
echo "Installing project requirements from requirements.txt..."
pip install -r requirements.txt

# Check if the installation was successful
if [ $? -eq 0 ]; then
    echo "Requirements successfully installed."
else
    echo "An error occurred while installing requirements."
    exit 1
fi

python3 scripts/__init__.py