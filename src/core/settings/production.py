from .base import *
import sys, logging

DEBUG = config("DEBUG", cast=bool, default=False)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',  # Log INFO level and higher messages
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
            'filters': []
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG', # Change the root logger to DEBUG
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG', # Explicitly set django.request to DEBUG
            'propagate': False,
        },

        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}


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
