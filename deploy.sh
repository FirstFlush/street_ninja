#!/bin/bash

# Street Ninja deploy script
# - Pulls latest code (unless --no-pull is passed)
# - Rebuilds Docker containers with .env.prod
# - Cleans up old images/containers
# - Starts the app

set -e

if [ "$EUID" -eq 0 ]; then
  echo "Do not run this script with sudo. Try it again as $USER."
  exit 1
fi

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
  echo "[1/7] Pulling latest changes from Git..."
  git pull origin master
else
  echo "[1/7] Skipping git pull (per --no-pull)"
fi

echo "[2/7] Stopping existing containers..."
docker compose down

echo "[3/7] Removing old containers and pruning images..."
docker compose rm -f
docker container prune -f
docker image prune -af
docker network prune -f

echo "[4/7] Rebuilding containers with .env.prod..."
docker compose --env-file $ENV_FILE build --no-cache

echo "[5/7] Running bootstrap tasks..."
docker compose --env-file $ENV_FILE run --rm bootstrap

echo "[6/7] Starting containers..."
docker compose --env-file $ENV_FILE up -d

echo "[7/7] Cleaning up build cache..."
docker builder prune --all --force

echo
echo "[SUCCESS] Deployment complete."
echo
echo "Reload Nginx server by running the command 'sudo systemctl reload nginx'"
