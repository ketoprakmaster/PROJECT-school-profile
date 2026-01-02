from pathlib import Path
from decouple import config

# --- Environment Configuration ---
LOG_LEVEL = config("LOG_LEVEL", default="INFO").upper()
LOG_FILE_PATH = config("LOG_FILE_PATH", default=None)
SENTRY_DSN = config("SENTRY_DSN", default=None)
ENVIRONMENT = config("ENVIRONMENT", "development").upper()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '%(levelname)s [%(asctime)s] %(name)s (%(lineno)d): '
                '%(message)s'
            ),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
        'django': {
            'handlers': ['console'],
            'level': config("DJANGO_LOG_LEVEL", default="INFO").upper(),
            'propagate': False,
        },
        # Prevent sensitive DB queries from flooding logs in prod
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# --- Production File Logging ---
if LOG_FILE_PATH:
    log_file = Path(LOG_FILE_PATH)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    LOGGING['handlers']['file'] = {
        'level': LOG_LEVEL,
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': str(log_file),
        'maxBytes': 1024 * 1024 * 10,  # 10 MB
        'backupCount': 5,
        'formatter': 'verbose',
    }
    LOGGING['loggers']['']['handlers'].append('file')

# --- Sentry SDK Initialization ---
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn = SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment = ENVIRONMENT,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=config("SENTRY_TRACE_RATE", default=0.1, cast=float),
        send_default_pii=True,
    )


# pyright: reportArgumentType=false
# pyright: reportAttributeAccessIssue=false
