# gunicorn.config.py

import multiprocessing

# Define the host and port to bind
bind = "0.0.0.0:8000"

# Number of worker processes for handling requests
# Use CPU cores * 2 + 1 for optimal performance
workers = multiprocessing.cpu_count() * 2 + 1

# Number of worker threads per process
threads = 2

# Maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50

# Enable access and error logging
accesslog = "-"
errorlog = "-"

# Log level (info, debug, warning, error, critical)
loglevel = "info"

# Enable graceful timeout for workers
timeout = 30
graceful_timeout = 30

# Preload app for faster worker startup
preload_app = True

# Set the working directory
chdir = "/app"

# Enable gunicorn to run in daemon mode (optional, not recommended in Docker)
# daemon = False
