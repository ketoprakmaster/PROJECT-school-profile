#!/bin/sh
# run the python application

python manage.py migrate
python manage.py auto_createsuperuser
python manage.py collectstatic --noinput
python -m gunicorn core.wsgi:application --bind 0.0.0.0:8000
