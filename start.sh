#!/bin/sh
set -e

echo "==> Running collectstatic..."
python manage.py collectstatic --noinput

echo "==> Running migrations..."
python manage.py migrate --noinput

echo "==> Seeding games..."
python manage.py seed_games

echo "==> Starting Gunicorn..."
exec gunicorn gameportal.wsgi --bind 0.0.0.0:$PORT --workers 2 --log-file -
