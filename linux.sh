#!/bin/bash

# Script to initialise project requirements

# Make sure files are executable
chmod +x linux_dist/activate_venv.sh
chmod +x linux_dist/install_requirements.sh

# Install create venv, install requirements
./linux_dist/activate_venv.sh
./linux_dist/install_requirements.sh

# Run the Python script
python3 scripts/__init__.py