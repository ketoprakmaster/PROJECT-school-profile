#!/bin/sh
# run the python application

# Run the Django management commands first
# INFO: ensure DJANGO_SETTINGS_MODULE set to the correct environment!
# otherwise it will NOT collectstatic to the correct place!
python manage.py migrate
python manage.py auto_createsuperuser
python manage.py collectstatic --noinput -v 3

# run the command passed via CMD
exec "$@"
