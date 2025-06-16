from .base import *

# Disable Debug Mode
DEBUG = False

# Static files configuration for production
STATIC_URL = '/static/'

# Collect static files into a single directory for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Databases for Production
DATABASES = {
    'default': {  # SQL Database (PostgreSQL/MySQL in Production)
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'api_monitor_db'),
        'USER': os.getenv('DB_USER', 'api_monitor_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'secure_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    },
    'mongo': {  # MongoDB for Production
        'ENGINE': 'djongo',
        'NAME': os.getenv('MONGO_DB_NAME', 'api_monitor_prod'),
        'CLIENT': {
            'host': os.getenv('MONGO_HOST', 'localhost'),
            'port': int(os.getenv('MONGO_PORT', 27017)),
            'username': os.getenv('MONGO_USER', ''),
            'password': os.getenv('MONGO_PASSWORD', ''),
            'authSource': os.getenv('MONGO_AUTH_DB', 'admin'),
        },
    },
}

# Allowed Hosts for Production
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# Security Settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
