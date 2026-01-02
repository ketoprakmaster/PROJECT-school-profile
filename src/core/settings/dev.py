from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# SECURITY WARNING: generate the apropriate secrets in PROD!
SECRET_KEY = "86d15f29-6235-402d-850a-f10490e88e1f-INSECURE!"

# use sqlite as a default backend for development
# if DATABASE hasn't been previously configured
if not DATABASES:
    DATABASES = {
            "default": {
                "ENGINE": DEFAULT_ENGINE,
                "NAME": BASE_DIR / "db.sqlite3",
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
