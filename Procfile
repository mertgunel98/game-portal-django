web: python manage.py collectstatic --noinput && python manage.py migrate --noinput && python manage.py seed_games && gunicorn gameportal.wsgi --bind 0.0.0.0:$PORT --workers 2 --log-file -
