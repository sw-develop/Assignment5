import json
import pathlib

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# 환경설정 파일을 불러온다.
try:
    with open(os.path.join(BASE_DIR, 'env/.env.dev_local.json'), "r", encoding='utf-8') as file:
        envs         = json.loads(file.read())
        SECRET_KEY   = envs.get('DJANGO_SECRET_KEY', 'secrect_key')
        OPEN_API_KEY = envs.get('OPEN_API_KEY', 'secrect_key')
except IOError as e:
    raise ImproperlyConfigured('env file not exist...')

LOGGING_BATCH_PATH = os.path.join(BASE_DIR, 'log/batch/batch.log')
LOGGING_COMMON_PATH = os.path.join(BASE_DIR, 'log/common/batch.log')

CRONJOBS = [
        ('* 0 * * *', 'research.crontab.start_batch', ),
]

CRONTAB_DJANGO_SETTINGS_MODULE = 'humanscape.settings.dev_local'

# Log의 경로 폴더를 만든다.
pathlib.Path(os.path.dirname(LOGGING_BATCH_PATH)).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.path.dirname(LOGGING_COMMON_PATH)).mkdir(parents=True, exist_ok=True)


LOGGING = {
    'version': 1,
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
    },

    'loggers': {
        'batch': {
            'handlers': ['batchfile'],
            'level': 'INFO',
        },
         'common': {
            'handlers': ['commonfile'],
            'level': 'INFO',
        },
    },

}