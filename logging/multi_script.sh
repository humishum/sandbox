#!/bin/bash

# Function to clean up background processes
cleanup() {
    echo "Cleaning up..."
    kill $(jobs -p) 2>/dev/null
    wait
}

# Trap SIGINT (Ctrl+C) and SIGTERM to run the cleanup function
trap cleanup SIGINT SIGTERM

# Start both scripts in parallel with close to 0 delay
python3 logging/logger1.py &  
python3 logging/logger2.py &  

# Wait for both to complete
wait
echo "Both scripts have completed."
