#!/bin/sh
#
# Wait for DB to be accepting requests before moving further.
#
# This script is executed as the Dockerfile's ENTRYPOINT.
set -e

# echo "Waiting for Postgres..."
# until pg_isready -h $DB_HOST -p 5432; do
# sleep 1
# done
# sleep 2

exec "$@"