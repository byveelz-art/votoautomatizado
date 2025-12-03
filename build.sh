#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install --upgrade pip
pip install -r requisitos.txt

# collect static files
python manage.py collectstatic --noinput

# apply migrations
python manage.py makemigrations
python manage.py migrate

    