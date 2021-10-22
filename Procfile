release: python manage.py flush --no-input
release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn settings.wsgi 