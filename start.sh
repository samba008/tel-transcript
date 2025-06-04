#!/bin/bash

# Start Gunicorn in the background
gunicorn transcriber_project.wsgi:application &

# Start Celery (connects to Redis)
celery -A transcriber_project worker --loglevel=info --pool=solo
