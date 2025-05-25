import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
CI = True if os.environ.get("CI").lower() == "true" else False
DEBUG = False if os.environ.get("DEBUG").lower() == "false" else True
ALLOWED_HOSTS = ["*"]

SMS_CHAR_LIMIT = os.environ.get("SMS_CHAR_LIMIT")

STREET_NINJA_WEBSITE_DOMAIN = os.environ.get("STREET_NINJA_WEBSITE_DOMAIN")
STREET_NINJA_API_DOMAIN = os.environ.get("STREET_NINJA_API_DOMAIN")

CACHE_DEFAULT_LOCATION = os.environ.get("CACHE_DEFAULT_LOCATION")
CACHE_SESSION_LOCATION = os.environ.get("CACHE_SESSION_LOCATION")
CACHE_PHONE_SESSION_LOCATION = os.environ.get("CACHE_PHONE_SESSION_LOCATION")
CACHE_RESOURCES_LOCATION = os.environ.get("CACHE_RESOURCES_LOCATION")
CACHE_CELERY_LOCATION = os.environ.get("CACHE_CELERY_LOCATION")
CACHE_LOCATION_LOCATION = os.environ.get("CACHE_LOCATION_LOCATION")
CACHE_TESTS_LOCATION = os.environ.get("CACHE_TESTS_LOCATION")

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# API Keys
# =======================================
GRAPH_HOPPER_API_KEY = os.environ.get("GRAPH_HOPPER_API_KEY")
NGROK_AUTH_TOKEN = os.environ.get("NGROK_AUTH_TOKEN")
NOMINATIM_USER_AGENT = os.environ.get("NOMINATIM_USER_AGENT")
OPENCAGE_API_KEY = os.environ.get("OPENCAGE_API_KEY")
OPEN_ROUTE_SERVICE_TOKEN = os.environ.get("OPEN_ROUTE_SERVICE_TOKEN")
VANCOUVER_OPEN_DATA_API_KEY = os.environ.get("VANCOUVER_OPEN_DATA_API_KEY")
WIGLE_API_KEY = os.environ.get("WIGLE_API_KEY")


# Email
# =======================================
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT"))
EMAIL_USE_TLS = True

EMAIL_ROUTE_CELERY = os.environ.get("EMAIL_ROUTE_CELERY")
EMAIL_ROUTE_DIRECTIONS = os.environ.get("EMAIL_ROUTE_DIRECTIONS")
EMAIL_ROUTE_LOCATION_PARSING = os.environ.get("EMAIL_ROUTE_LOCATION_PARSING")
EMAIL_ROUTE_LOGGING = os.environ.get("EMAIL_ROUTE_LOGGING")
EMAIL_ROUTE_SENTRY = os.environ.get("EMAIL_ROUTE_SENTRY")


# Celery
# =======================================
CELERY_BROKER_URL = ""
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


# CORS 
# =======================================
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGIN_REGEXES = [r"^https?:\/\/.*"]


# Geocoding
# =======================================
GEOCODER_CONFIG = {
    "NOMINATIM": {"user_agent": ""},
    "OPENCAGE": {"api_key": ""},
}
PRIMARY_GEOCODER = ""


# PERMISSIONS
# =======================================
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}


# PHONE SESSION
# =======================================
TTL_PHONE_SESSION = os.environ.get("TTL_PHONE_SESSION")


# Routes
# =======================================
ROUTE_ADMIN = os.environ.get("ROUTE_ADMIN")
ROUTE_SMS_GATEWAY = os.environ.get("ROUTE_SMS_GATEWAY")


# Twilio
# =======================================
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_celery_beat',
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'cache',
    'common',
    'contacts',
    'geo',
    'integrations',
    'notifications',
    'resources',
    'sms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'street_ninja_server.urls'
WSGI_APPLICATION = 'street_ninja_server.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "test_db",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'phone_session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'resources': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/3',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'celery': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/4',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'geo': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/5',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'tests': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/6',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}



# Add the bare minimum to boot Django
STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
