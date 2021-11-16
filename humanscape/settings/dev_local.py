from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'secrect_key')

OPEN_API_AUTH_KEY = os.environ.get('OPEN_API_AUTH_KEY', 'auth_key')

OPEN_API_SERVICE_KEY = os.environ.get('OPEN_API_SERVICE_KEY', 'service_key')

LOGGING_BATCH_PATH = os.path.join(BASE_DIR, 'log/batch/batch.log')
LOGGING_COMMON_PATH = os.path.join(BASE_DIR, 'log/common/batch.log')

SERVER_EMAIL = "notification@assignment5.com"
#ADMINS = [('', ''), ]


CRONJOBS = [
        #('* 0 * * *', 'research.get_data_from_db', >> .log/cron.log'),
        ('*/1 * * * *', 'research.batch.start_batch'),
]

CRONTAB_DJANGO_SETTINGS_MODULE = 'humanscape.settings.dev_local'
#CRONTAB_LOCK_JOBS = True


# logging
LOGGING = {
    'version': 1,
    # 기존의 로깅 설정을 비활성화 할 것인가?
    'disable_existing_loggers': False,

    # 포맷터
    # 로그 레코드는 최종적으로 텍스트로 표현됨
    # 이 텍스트의 포맷 형식 정의
    # 여러 포맷 정의 가능
    'formatters': {
        'format': {
            'format': '[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },

    # 핸들러
    # 로그 레코드로 무슨 작업을 할 것인지 정의
    # 여러 핸들러 정의 가능
    'handlers': {
        # 로그 파일을 만들어 텍스트로 로그레코드 저장
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

    # 로그 레코드 저장소
    # 로거를 이름별로 정의
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
