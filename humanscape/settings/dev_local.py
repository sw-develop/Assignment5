from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'secrect_key')

OPEN_API_AUTH_KEY = os.environ.get('OPEN_API_AUTH_KEY', 'auth_key')

OPEN_API_SERVICE_KEY = os.environ.get('OPEN_API_SERVICE_KEY', 'service_key')
