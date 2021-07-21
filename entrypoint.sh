#!/bin/bash

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py initadmin
python manage.py initmarks

gunicorn "$DJANGO_SETTINGS_FOLDER".wsgi