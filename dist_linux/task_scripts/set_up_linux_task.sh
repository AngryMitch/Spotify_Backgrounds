#!/bin/bash

# Define variables
EXECUTABLE_PATH="$HOME/Documents/Python_BG/dist_linux/__init__/__init__"
CRON_JOB="0 2 * * * $EXECUTABLE_PATH"

# Check if the executable exists
if [ ! -f "$EXECUTABLE_PATH" ]; then
    echo "Executable not found: $EXECUTABLE_PATH"
    exit 1
fi

# Add cron job if it doesn't already exist
(crontab -l 2>/dev/null | grep -v -F "$EXECUTABLE_PATH"; echo "$CRON_JOB") | crontab -

echo "Cron job added to run daily at 2:00 AM."