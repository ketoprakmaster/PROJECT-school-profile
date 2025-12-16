from decouple import config
from storages.backends.s3boto3 import S3Boto3Storage

# Default storage settings
# See https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-STORAGES

class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    querystring_auth = False  # Static files should have clean URLs for caching

class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'   # Keeps user uploads secure
    file_overwrite = False
    querystring_auth = True   # Generates temporary signed links for security

# Gather credentials
S3_BUCKET_NAME = config("S3_BUCKET_NAME", default=None)
S3_ENDPOINT_URL = config("S3_ENDPOINT_URL", default=None)
S3_ACCESS_KEY = config("S3_ACCESS_KEY", default=None)
S3_SECRET_KEY = config("S3_SECRET_KEY", default=None)
S3_CUSTOM_DOMAIN = config("S3_CUSTOM_DOMAIN", default=None)
S3_REGION_NAME = config("S3_REGION_NAME", default="auto")

# Initialize options only if all required keys are present
USE_S3 = all([S3_BUCKET_NAME, S3_ENDPOINT_URL, S3_ACCESS_KEY, S3_SECRET_KEY])

if USE_S3:
    S3_CONFIG_OPTIONS = {
        "bucket_name": S3_BUCKET_NAME,
        "access_key": S3_ACCESS_KEY,
        "secret_key": S3_SECRET_KEY,
        "endpoint_url": S3_ENDPOINT_URL,
        "region_name": S3_REGION_NAME,
        "signature_version": "s3v4",
        "custom_domain": S3_CUSTOM_DOMAIN, # Tells Django to use your domain for URLs
        "object_parameters": {
            'CacheControl': 'max-age=2592000', # 30 days
        },
    }

if USE_S3:
    STORAGES = {
        'default': {
            'BACKEND': 'core.configs.storages.MediaStorage',
            'OPTIONS': S3_CONFIG_OPTIONS,
        },
        'staticfiles': {
            'BACKEND': 'core.configs.storages.StaticStorage',
            'OPTIONS': S3_CONFIG_OPTIONS,
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
        },
    }

# URL configuration
if USE_S3 and S3_CUSTOM_DOMAIN:
    STATIC_URL = f"{S3_CUSTOM_DOMAIN}/static/"
    MEDIA_URL = f"{S3_CUSTOM_DOMAIN}/media/"
else:
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
