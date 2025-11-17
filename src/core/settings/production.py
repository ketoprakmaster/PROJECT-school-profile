from .base import *
import sys, logging

DEBUG = config("DEBUG", cast=bool, default=False)

if config("LOGGING", cast=bool, default=True):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                        'pathname=%(pathname)s lineno=%(lineno)s ' +
                        'funcname=%(funcName)s %(message)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'testlogger': {
                'handlers': ['console'],
                'level': 'INFO',
            }
        }
    }

DEBUG_PROPAGATE_EXCEPTIONS = config("DEBUG_PROPAGATE_EXCEPTIONS",cast=bool,default=False)
COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)


# configure the apss domains
CSRF_TRUSTED_ORIGINS = [
    "https://*.noodlefish-hen.ts.net",
    "https://*.railway.app"
]

ALLOWED_HOSTS = [
    ".railway.app",
    ".noodlefish-hen.ts.net",

    '127.0.0.1',
    '.localhost'
]


try:
    from .local import *
except ImportError:
    pass
