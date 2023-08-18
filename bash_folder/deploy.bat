@echo off

REM Change to the directory where the script is located
cd /d "%~dp0"

REM Get the current folder name
for %%I in ("%cd%") do set "folder_name=%%~nxI"
REM Build Docker images
docker build -t %folder_name%-actions-image -f Dockerfile.actions .
docker build -t %folder_name%-rasa-os-image -f Dockerfile.rasa-os .

REM Run docker compose up command
docker compose up
