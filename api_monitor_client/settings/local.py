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
    }
}

# Allowed Hosts for Dev
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

