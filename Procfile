web: python manage.py migrate --noinput && python manage.py createsuperuser --noinput 2>/dev/null; gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
