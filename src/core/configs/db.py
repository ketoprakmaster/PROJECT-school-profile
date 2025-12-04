from decouple import config
from core.configs.paths import BASE_DIR

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# try use a configured database url if it exists

DEFAULT_ENGINE = "django.db.backends.sqlite3"

DB_ENGINE = config("DB_ENGINE", default=DEFAULT_ENGINE)
DB_NAME = config("DB_NAME", default=None)
DB_USER = config("DB_USER", default=None)
DB_PASSWORD = config("DB_PASSWORD", default=None)
DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", default=None)

if DB_NAME and DB_USER and DB_PASSWORD:
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
            "CONN_MAX_AGE": config("DB_CONN_MAX_AGE", cast=int, default=600),
            "CONN_HEALTH_CHECKS": config("DB_CONN_HEALTH_CHECKS", cast=bool, default=True),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": DEFAULT_ENGINE,
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
