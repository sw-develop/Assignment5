import json
import pathlib

from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'secrect_key')

OPEN_API_AUTH_KEY = os.environ.get('OPEN_API_AUTH_KEY', 'auth_key')

OPEN_API_SERVICE_KEY = os.environ.get('OPEN_API_SERVICE_KEY', 'service_key')

LOGGING_BATCH_PATH = os.path.join(BASE_DIR, 'log/batch/batch.log')
LOGGING_COMMON_PATH = os.path.join(BASE_DIR, 'log/common/batch.log')

SERVER_EMAIL = "notification@assignment5.com"

ADMINS_INFO_FILE_NAME = os.environ.get('ADMINS_INFO', 'admins_info.json')

ADMINS = []

try:
    with open(os.path.join(BASE_DIR, ADMINS_INFO_FILE_NAME), "r") as file:
        admin_info = json.load(file)
        ADMINS = [(info['name'], info['email']) for info in admin_info]
except KeyError:
    raise ImproperlyConfigured('Invalid json file format')
except IOError as e:
    print(f'Admin info file ({ADMINS_INFO_FILE_NAME}) not exist continue runserver...')


CRONJOBS = [
        ('*/1 * * * *', 'research.batch.start_batch'),
]

CRONTAB_DJANGO_SETTINGS_MODULE = 'humanscape.settings.deploy'

pathlib.Path(os.path.dirname(LOGGING_BATCH_PATH)).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.path.dirname(LOGGING_COMMON_PATH)).mkdir(parents=True, exist_ok=True)


LOGGING = {
    'version': 1,
    # 기존의 로깅 설정을 비활성화 할 것인가?
    'disable_existing_loggers': False,
    'formatters': {
        'format': {
            'format': '[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },

    'handlers': {
        'batchfile': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'W0',
            'filename': LOGGING_BATCH_PATH,
            'formatter': 'format',
        },

         'commonfile': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when' : 'D',
            'filename': LOGGING_COMMON_PATH,
            'formatter': 'format',
        },

        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    
    },

    'loggers': {
        'batch': {
            'handlers': ['batchfile', 'mail_admins'],
            'level': 'INFO',
        },
         'research': {
            'handlers': ['commonfile'],
            'level': 'INFO',
        },
    },

}
