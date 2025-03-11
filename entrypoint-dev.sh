#!/bin/bash

set -e

# Activate virtual environment
source venv/bin/activate

# Start Celery worker
celery -A mysite worker -l INFO --detach

# Start Celery beat
celery -A mysite beat -l INFO --detach

# Start Django application
exec python manage.py runserver 0.0.0.0:8000
