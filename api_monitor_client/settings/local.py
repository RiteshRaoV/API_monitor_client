from .base import *

# Enable Debug Mode
DEBUG = True

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = '/app/static/' 
# Databases Configuration
DATABASES = {
    'default': {  # SQL Database (PostgreSQL/MySQL/SQLite for Dev)
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mongo': {  # MongoDB Configuration
        'ENGINE': 'djongo',
        'NAME': os.getenv('MONGO_DB_NAME', 'api_monitor_local'),
        'CLIENT': {
            'host': os.getenv('MONGO_HOST', 'localhost'),
            'port': int(os.getenv('MONGO_PORT', 27017)),
            'username': os.getenv('MONGO_USER', ''),
            'password': os.getenv('MONGO_PASSWORD', ''),
            'authSource': os.getenv('MONGO_AUTH_DB', 'admin'),
        },
    },
}

# Allowed Hosts for Dev
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Enable Django Debug Toolbar (optional)
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

import socket

# Docker internal IP fix for Debug Toolbar
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = ['127.0.0.1', 'localhost', '0.0.0.0'] + [ip[:-1] + '1' for ip in ips]

