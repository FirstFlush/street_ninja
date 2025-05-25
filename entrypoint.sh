#!/bin/sh
#
# Entrypoint script for the Django container.
# - Waits for Postgres
# - Applies database migrations
# - Loads neighborhoods
# - Starts Gunicorn
#
# This script is executed as the Dockerfile's ENTRYPOINT.
set -e

if [ "$CI" != "True" ]; then
    echo "Waiting for Postgres..."
    until pg_isready -h db -p 5432; do
    sleep 1
    done
    sleep 2

    echo "Applying database migrations..."
    python manage.py migrate

    echo "Running get_locations..."
    python manage.py get_neighborhoods
else
    echo "CI environment detected, skipping entrypoint.sh setup logic..."
fi

echo "Starting server..."
exec "$@"