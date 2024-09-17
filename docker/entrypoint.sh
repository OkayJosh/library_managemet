#!/usr/bin/env bash

# Navigate to the project directory
PROJECT_DIR="$WORKDIR"
echo "Changing to project directory: ${PROJECT_DIR}..."
cd "${PROJECT_DIR}" || {
    echo "Failed to change to project directory. Exiting." >&2
    exit 1
}

# Log start of script
echo "Starting Django application setup..."

# Source the .env file and export environment variables
echo "Loading environment variables from .env file..."
if ! export $(grep -v '^#' .env | xargs); then
    echo "Failed to export environment variables from .env file. Exiting." >&2
    exit 1
fi

# Check if the database is reachable
echo "Checking if the database is reachable..."
if ! docker/reach_database.sh; then
    echo "Database is not reachable. Exiting." >&2
    exit 1
fi

# Collect static files
#echo "Collecting static files..."
#python manage.py collectstatic --noinput || { echo "Failed to collect static files. Exiting."; exit 1; }
#echo "Static files collected."

# NOTE: i moved running migrations to the celery worker.
# NOTE: why because this is where most of the actions occurs
# Apply database migrations for multiple databases
#DATABASES=("${POSTGRES_DB_1}" "${POSTGRES_DB_2}")
#for DB in "${DATABASES[@]}"; do
#    echo "Running database migrations for database: ${DB}..."
#    if ! python manage.py migrate --database="${DB}"; then
#        echo "Database migrations for ${DB} failed. Exiting." >&2
#        exit 1
#    fi
#done

# Start Gunicorn server
echo "Starting Gunicorn server..."
gunicorn library_managemet.wsgi:application \
    --bind ":${GUNICORN_PORT:-8000}" \
    --workers "${GUNICORN_WORKERS:-3}" \
    --log-level "${GUNICORN_LOG_LEVEL:-info}" \
    --access-logfile '-' \
    --error-logfile '-' \
    --timeout "${GUNICORN_TIMEOUT:-30}"

# Log successful start
echo "Gunicorn server started on port ${GUNICORN_PORT:-8000}."
