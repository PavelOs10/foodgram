#!/bin/bash
set -e

echo "=== Starting Foodgram Application ==="

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 foodgram.wsgi:application