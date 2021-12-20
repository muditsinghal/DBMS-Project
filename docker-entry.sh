#!/bin/bash

# Collect static files
echo "Collect static files"
python3 Carpooling/manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python Carpooling/manage.py migrate

# Start server
echo "Starting server"
python Carpooling/manage.py runserver 0.0.0.0:8000