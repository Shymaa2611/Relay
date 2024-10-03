release: python manage.py migrate & python manage.py colletstatic
web: daphne Project.asgi:application --port $PORT --bind 0.0.0.0 -v2
