#!/bin/bash
#cd /app/backend
#$SHELL
#/bin/sh -c "pwd"
#/bin/sh -c "ls -l"
/bin/sh -c "until nc -z db 5432; do sleep 1; done"
/bin/sh -c "python manage.py migrate"
/bin/sh -c "python manage.py createsuperuser --noinput --username chelen --email zelen@gmail.com"
/bin/sh -c "gunicorn backend.wsgi:application --bind 0.0.0.0:8000"