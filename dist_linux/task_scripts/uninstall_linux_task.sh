#!/bin/bash

# Define variables
EXECUTABLE_PATH="$HOME/Documents/Python_BG/dist_linux/__init__/__init__"

# Check if the executable exists
if [ ! -f "$EXECUTABLE_PATH" ]; then
    echo "Executable not found: $EXECUTABLE_PATH"
    exit 1
fi

# Remove the cron job
crontab -l 2>/dev/null | grep -v -F "$EXECUTABLE_PATH" | crontab -

echo "Cron job removed."