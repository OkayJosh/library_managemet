FROM ubuntu:latest
LABEL authors="Joshua Olatunji"

# Use the official Python image as a base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE library_managemet.settings

# Set the working directory in the container
WORKDIR /lb

# Optional: Set WORKDIR as an environment variable so it's available in scripts
ENV WORKDIR /lb

# Copy the current directory contents into the container at /lb
COPY . /lb

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for Celery files and set permissions
RUN mkdir -p /var/run/lb && \
    chown -R www-data:www-data /var/run/lb

# Create the staticfiles directory and set the ownership to www-data
RUN mkdir -p /lb/staticfiles && \
    chown -R www-data:www-data /lb/staticfiles

# Set appropriate permissions for the application directory
RUN chown -R www-data:www-data /lb

# Set executable permissions for entrypoint.sh and reach_database.sh
RUN chmod +x /lb/docker/entrypoint.sh
RUN chmod +x /lb/docker/entrypoint.second.sh
RUN chmod +x /lb/docker/celery.worker.entrypoint.sh
RUN chmod +x /lb/docker/reach_database.sh

# Switch to non-root user
USER www-data