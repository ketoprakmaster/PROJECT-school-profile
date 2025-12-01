#!/bin/sh
# run the python application

# Run the Django management commands first
python manage.py migrate
python manage.py auto_createsuperuser
python manage.py collectstatic --noinput

# run the command passed via CMD
exec "$@"
