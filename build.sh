#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install --upgrade pip
pip install -r requisitos.txt

# collect static files
python manage.py collectstatic --noinput

# apply migrations
python manage.py migrate
# create superuser if not exists
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
if not User.objects.filter(username='admin').exists(): \
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')" | python manage.py shell
# start server
python manage.py runserver votoautomatizado.onrender.com:8000
    