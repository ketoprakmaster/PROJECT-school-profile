from .base import *
from core.configs.logs import LOGGING

from decouple import config, Csv

DEBUG = config("DEBUG", cast=bool, default=False)
DEBUG_PROPAGATE_EXCEPTIONS = config("DEBUG_PROPAGATE_EXCEPTIONS",cast=bool,default=False)
COMPRESS_ENABLED = config('COMPRESS_ENABLED', cast=bool, default=False)

# configure the apps domains
CSRF_TRUSTED_ORIGINS = config("CRSF_TRUSTED_ORIGINS", cast=Csv(), default="http://localhost:8000, http://127.0.0.1:8000")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="localhost, 127.0.0.1")

# raise ValueError if secret keys do not exist
SECRET_KEY = config("SECRET_KEY")

# HTTPS/Security Settings
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", cast=bool, default=False)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", cast=bool, default=False)
X_FRAME_OPTIONS = "DENY"

# HSTS settings
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", cast=int, default=0) # Recommend 1 year default
SECURE_HSTS_INCLUDE_SUBDOMAINS = config("SECURE_HSTS_INCLUDE_SUBDOMAINS", cast=bool, default=False)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", cast=bool, default=False)

# SSL/Proxy settings
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", cast=bool, default=False)
USE_X_FORWARDED_HOST = config("USE_X_FORWARDED_HOST", cast=bool, default=False)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Logging Configuration
if LOGGING:
    DJANGO_LOGGING = LOGGING

try:
    from .local import *
except ImportError:
    pass

# pyright: reportOperatorIssue=false
