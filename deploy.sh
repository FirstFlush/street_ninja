#!/bin/bash

# Street Ninja deploy script
# - Pulls latest code (unless --no-pull is passed)
# - Rebuilds Docker containers with .env.prod
# - Cleans up old images/containers
# - Starts the app

set -e  # Exit on error

ENV_FILE=".env.prod"

if [ ! -f "$ENV_FILE" ]; then
  echo ".env.prod file not found. Deployment may fail if required variables are missing."
  read -p "Continue anyway? [y/N]: " confirm
  if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Exiting deployment."
    exit 1
  fi
fi

SKIP_PULL=false
if [[ "$1" == "--no-pull" ]]; then
  SKIP_PULL=true
fi

sudo -v  # trigger sudo auth upfront

echo "Starting deployment..."

if [ "$SKIP_PULL" = false ]; then
  echo "[1/6] Pulling latest changes from Git..."
  git pull origin master
else
  echo "[1/6] Skipping git pull (per --no-pull)"
fi

echo "[2/6] Stopping existing containers..."
docker compose down

echo "[3/6] Removing old containers and pruning images..."
docker compose rm -f
docker container prune -f
docker image prune -af
docker network prune -f

echo "[4/6] Rebuilding containers with .env.prod..."
docker compose --env-file $ENV_FILE build --no-cache

echo "[5/6] Starting containers..."
docker compose --env-file $ENV_FILE up -d

echo "Deployment complete. Reload Nginx server by running the command 'sudo systemctl reload nginx'"
