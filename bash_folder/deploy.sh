#!/bin/bash

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Get the current folder name
folder_name="$(basename "$PWD")"

# Build Docker images
docker build -t "$folder_name-actions-image" -f "$folder_name/Dockerfile.actions" .
docker build -t "$folder_name-rasa-os-image" -f "$folder_name/Dockerfile.rasa-os" .

# Run docker compose up command
docker compose up
