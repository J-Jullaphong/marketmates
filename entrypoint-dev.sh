#!/bin/bash

set -e

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Start Celery worker
celery -A mysite worker -l INFO --detach

# Start Celery beat
celery -A mysite beat -l INFO --detach

# Start Django application
exec python manage.py runserver 0.0.0.0:8000
