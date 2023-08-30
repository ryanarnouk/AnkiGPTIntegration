#!/bin/bash

stop_container() {
    docker stop anki-gpt-integration
    exit
}

trap stop_container INT

(
    # Run the frontend build
    cd ./client

    # Serve the client 
    npx serve -s build
) & 

# Step 1: Run run the Python server Docker container
docker start -a anki-gpt-integration