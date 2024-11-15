#!/bin/sh

# Create and set permissions for coverage directory
mkdir -p /app/cov
chmod 777 /app/cov

# Switch to django-user during server start
exec su django-user -c "python manage.py wait_for_db && python manage.py runserver 0.0.0.0:8000"
