#!/bin/bash

set -e

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Apply database migrations
python manage.py migrate

# Start Celery worker
celery -A mysite worker -l INFO --detach

# Start Celery beat
celery -A mysite beat -l INFO --detach

# Collect Static files
python manage.py collectstatic --noinput

# Start Daphne
nohup daphne -b 0.0.0.0 -p 8001 mysite.asgi:application > daphne.log 2>&1 &

# Start Gunicorn
exec gunicorn --workers 4 --bind 0.0.0.0:8000 mysite.wsgi:application
