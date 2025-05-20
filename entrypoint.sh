#!/bin/sh
#
# Entrypoint script for the Django container.
# - Applies database migrations
# - Runs the get_neighborhoods management command to populate Neighborhood table
# - Starts the main server process (e.g., Gunicorn)
#
# This script is executed as the Dockerfile's ENTRYPOINT.
set -e

echo "Applying database migrations..."
python manage.py migrate

echo "Running get_locations..."
python manage.py get_neighborhoods

echo "Starting server..."
exec "$@"
