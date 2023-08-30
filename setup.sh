#!/bin/bash

# Step 1: Grab environment variables
if [[ -f .env ]]; then
  source .env
fi

stop_container() {
    docker stop anki-gpt-integration
    exit
}

trap stop_container INT

# Step 2: Build and run the Python server Docker container
docker build -t anki-gpt-integration-server --build-arg open_api_key=$OPEN_API_KEY .
docker run -d --name anki-gpt-integration -p 105:105 anki-gpt-integration-server

cd ./client

npm install 

npm run build

npm install serve

npx serve -s build
