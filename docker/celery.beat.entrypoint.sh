#!/bin/bash

# Make the database check script executable
chmod +x ./reach_database.sh

# Navigate to the project directory
PROJECT_DIR="$HOME/library_managemet"
PROJECT_DIR="$HOME/lycon/library_managemet"
echo "Changing to project directory: ${PROJECT_DIR}..."
cd "${PROJECT_DIR}" || {
    echo "Failed to change to project directory. Exiting." >&2
    exit 1
}

# Source the .env file, ensuring variables are exported correctly
# shellcheck disable=SC2046
export $(grep -v '^#' .env | xargs)

# Run the script to check if the database is reachable
echo "Checking if the database is reachable..."
docker/reach_database.sh || {
    echo "Database is not reachable. Exiting." >&2
    exit 1
}

# Run Django system health check
echo "Performing Django system checks..."
python manage.py check || {
    echo "Django check failed. Exiting." >&2
    exit 1
}

# Create the Celery Beat PID directory if it doesn't exist
echo "Setting up Celery Beat directories..."
mkdir -p /var/run/library_managemet
if [[ $? -ne 0 ]]; then
    echo "Failed to create directory /var/run/library_managemet. Exiting." >&2
    exit 1
fi

# Ensure the current user owns the Celery directory
chown "$USER:$USER" /var/run/library_managemet

# Start Celery Beat
echo "Starting Celery Beat..."
exec celery --app=library_managemet \
    beat \
    --pidfile=/var/run/library_managemet/celery-beat.pid \
    --schedule=/var/run/library_managemet/celerybeat-schedule || {
    echo "Failed to start Celery Beat. Exiting." >&2
    exit 1
}
