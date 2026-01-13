from .base import *
from django.core.management.utils import get_random_secret_key
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# SECURITY WARNING: generate the apropriate secrets in PROD!
SECRET_KEY = config("SECRET_KEY", get_random_secret_key())

# use sqlite as a default backend for development
# if DATABASE hasn't been previously configured
if not DATABASES:
    # ensure the parents path exists
    DB_DIR = BASE_DIR / "data"
    DB_DIR.mkdir(parents=True, exist_ok=True)

    DATABASES = {
            "default": {
                "ENGINE": DEFAULT_ENGINE,
                "NAME": DB_DIR / "db.sqlite3",
            }
        }

# override the storages for static assets to be FileSystemStorage
# recomended for tailwind dynamic compiling in development
STORAGES["staticfiles"] = {
    "BACKEND" : "django.contrib.staticfiles.storage.StaticFilesStorage"
}


try:
    from .local import *
except ImportError:
    pass
