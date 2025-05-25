from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "dzl2wt+uxvg16wk=64$s1l#nhjtvld#1q-z945i#16+$=xhlt9"
CI = True
DEBUG = False
ALLOWED_HOSTS = ["*"]

SMS_CHAR_LIMIT = 300

STREET_NINJA_WEBSITE_DOMAIN="streetninja.ca"
STREET_NINJA_API_DOMAIN="api.streetninja.ca"

CACHE_DEFAULT_LOCATION="redis://street_ninja_redis:6379/0"
CACHE_SESSION_LOCATION="redis://street_ninja_redis:6379/1"
CACHE_PHONE_SESSION_LOCATION="redis://street_ninja_redis:6379/2"
CACHE_RESOURCES_LOCATION="redis://street_ninja_redis:6379/3"
CACHE_CELERY_LOCATION="redis://street_ninja_redis:6379/4"
CACHE_LOCATION_LOCATION="redis://street_ninja_redis:6379/5"
CACHE_TESTS_LOCATION="redis://street_ninja_redis:6379/6"

DB_NAME="test_db"
DB_USER="postgres"
DB_PASS="postgres"
DB_HOST="postgres"
DB_PORT="5432"

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# API Keys
# =======================================
GRAPH_HOPPER_API_KEY = "FAKE_GRAPH_HOPPER_API_KEY"
NGROK_AUTH_TOKEN = "FAKE_NGROK_AUTH_TOKEN"
NOMINATIM_USER_AGENT = "FAKE_NOMINATUM_USER_AGENT"
OPENCAGE_API_KEY = "FAKE_OPENCAGE_API_KEY"
OPEN_ROUTE_SERVICE_TOKEN = "FAKE_OPEN_ROUTE_SERVICE_TOKEN"
VANCOUVER_OPEN_DATA_API_KEY = "FAKE_VANCOUVER_OPEN_DATA_API_KEY"
WIGLE_API_KEY = "FAKE_WIGLE_API_KEY"


# Email
# =======================================
EMAIL_HOST_USER = "fake@streetninja.ca"
EMAIL_HOST_PASSWORD = "FAKE_EMAIL_PASSWORD"
EMAIL_HOST = "FAKE_EMAIL_HOST.ca"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_ROUTE_CELERY = "celery-fake"
EMAIL_ROUTE_DIRECTIONS = "directions-fake"
EMAIL_ROUTE_LOCATION_PARSING = "location-parsing-fake"
EMAIL_ROUTE_LOGGING = "logging-fake"
EMAIL_ROUTE_SENTRY = "sentry-fake"


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
TTL_PHONE_SESSION = 3600


# Routes
# =======================================
ROUTE_ADMIN="admin-fake/"
ROUTE_SMS_GATEWAY="sms-gateway-fake/"


# Twilio
# =======================================
TWILIO_PHONE_NUMBER="FAKE_TWILIO_PHONE_NUMBER"
TWILIO_ACCOUNT_SID="FAKE_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN="FAKE_TWILIO_AUTH_TOKEN"


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
