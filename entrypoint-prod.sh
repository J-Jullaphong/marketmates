#!/bin/bash

set -e

# Activate virtual environment
source venv/bin/activate

# Start Celery worker
celery -A mysite worker -l INFO --detach

# Start Celery beat
celery -A mysite beat -l INFO --detach

# Collect Static files
python manage.py collectstatic --noinput

# Start Django application
exec daphne -b 0.0.0.0 -p 8000 mysite.asgi:application
