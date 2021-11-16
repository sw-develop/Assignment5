import json
import pathlib

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# 환경설정 파일을 불러온다.
try:
    with open(os.path.join(BASE_DIR, 'env/.env.deploy.json'), "r", encoding='utf-8') as file:
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

CRONTAB_DJANGO_SETTINGS_MODULE = 'humanscape.settings.deploy'

# Log의 경로 폴더를 만든다.
pathlib.Path(os.path.dirname(LOGGING_BATCH_PATH)).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.path.dirname(LOGGING_COMMON_PATH)).mkdir(parents=True, exist_ok=True)

# 관리자에게 보낼 이메일의 발신자
SERVER_EMAIL = "notification@assignment5.com"

# 서버의 에러가 나면 연락 할 관리자 정보 [('관리자이름', '이메일'), ....]
ADMINS = []
try:
    with open(os.path.join(BASE_DIR, 'env/.env.admin_info.json'), "r", encoding='utf-8') as file:
        admin_info = json.loads(file.read())
        ADMINS = [(info['name'], info['email']) for info in admin_info]
except KeyError:
    raise ImproperlyConfigured('Invalid json file format')
except IOError as e:
    print('Admin info file not exist continue runserver...')


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
         'common': {
            'handlers': ['commonfile'],
            'level': 'INFO',
        },
    },

}