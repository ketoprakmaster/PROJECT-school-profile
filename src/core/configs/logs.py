# configs/logs.py

from decouple import config
from core.configs.paths import BASE_DIR, Path

# --- Environment Configuration ---
LOG_LEVEL = str(config("LOG_LEVEL", default="INFO")).upper()
LOG_FILE_PATH = config("LOG_FILE_PATH", default=None)

# -----------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # 1. Formatters: Define how the log messages look
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

    # 2. Handlers: Define where the log messages go
    'handlers': {
        # Console Handler (Always active, useful for Docker logs)
        'console': {
            'level': 'DEBUG', # Always capture DEBUG, filter by logger level
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },

    # 3. Loggers: Define which parts of the code log messages and at what level
    'loggers': {
        # Default application logger (catches everything not handled below)
        '': {
            'handlers': ['console'],
            'level': LOG_LEVEL, # Controlled by environment variable
            'propagate': True,
        },
        # Django's own core logger
        'django': {
            'handlers': ['console'],
            'level': 'WARNING', # Set Django warnings and errors to a higher level
            'propagate': False,
        },
        # Specific logger for database queries/operations
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO', # Set to INFO/DEBUG for development
            'propagate': False,
        },
    }
}

# --- Production File Logging Extension ---
# Only add file logging if a LOG_FILE_PATH is provided (e.g., in production)
if LOG_FILE_PATH:
    # Ensure the directory exists
    log_dir = Path(LOG_FILE_PATH)
    log_dir.mkdir(parents=True,exist_ok=True)

    # Add the File Handler to the handlers dictionary
    LOGGING['handlers']['file'] = {
        'level': LOG_LEVEL,
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': LOG_FILE_PATH,
        'maxBytes': 1024 * 1024 * 5,  # 5 MB
        'backupCount': 5,            # Keep 5 backup files
        'formatter': 'verbose',
    }

    # Update the root logger to also use the file handler
    LOGGING['loggers']['']['handlers'] = ['console', 'file']
    # Update the Django logger to also use the file handler
    LOGGING['loggers']['django']['handlers'] = ['console', 'file']
