web: gunicorn Project.asgi:application --bind 0.0.0.0:$PORT --workers 3 --worker-class="uvicorn.workers.UvicornWorker"
worker: daphne Project.asgi:application --port $PORT --bind 0.0.0.0 -v2
