"""
Django settings for street_ninja_server project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from .logging_config import LOGGING


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'log'
os.makedirs(LOG_DIR, exist_ok=True)
LOGGING = LOGGING
LOGGING['handlers']['file']['filename'] = f"{LOG_DIR}/street_ninja.log"

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
CI = False
DEBUG = True if os.environ.get("DEBUG", "").lower() == "true" else False

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = [
        "api.streetninja.ca",
        "streetninja.ca",
        "www.streetninja.ca",
        "206.81.12.149",
        "localhost",
        "127.0.0.1",
        "street_ninja_web",
        "web",
    ]

APPEND_SLASH = False
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# API Keys
# =======================================
VANCOUVER_OPEN_DATA_API_KEY = os.environ.get('VANCOUVER_OPEN_DATA_API_KEY')
WIGLE_API_KEY = os.environ.get('WIGLE_API_KEY')
OPEN_ROUTE_SERVICE_TOKEN = os.environ.get('OPEN_ROUTE_SERVICE_TOKEN')
GRAPH_HOPPER_API_KEY = os.environ.get('GRAPH_HOPPER_API_KEY')


# Domain
# =======================================
STREET_NINJA_WEBSITE_DOMAIN = os.environ.get("STREET_NINJA_WEBSITE_DOMAIN")
STREET_NINJA_API_DOMAIN = os.environ.get("STREET_NINJA_API_DOMAIN")


# EMAIL CONFIG
# =======================================
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", ""))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True  # always, no need for env var


# EMAIL ROUTES
# =======================================
EMAIL_ROUTE_CELERY = os.environ.get("EMAIL_ROUTE_CELERY")
EMAIL_ROUTE_DIRECTIONS = os.environ.get("EMAIL_ROUTE_DIRECTIONS")
EMAIL_ROUTE_LOCATION_PARSING = os.environ.get("EMAIL_ROUTE_LOCATION_PARSING")
EMAIL_ROUTE_LOGGING = os.environ.get("EMAIL_ROUTE_LOGGING")
EMAIL_ROUTE_SENTRY = os.environ.get("EMAIL_ROUTE_SENTRY")


# Sentry
# =======================================
if not DEBUG:
    import sentry_sdk
    sentry_sdk.init(
        dsn="https://57fe7909f58441a08c24f9de1da36ebc@o4509062836060160.ingest.us.sentry.io/4509062856572928",
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
    )


# SMS
# =======================================
SMS_CHAR_LIMIT = int(os.environ.get('SMS_CHAR_LIMIT', 400))
END_OF_RESULTS = "End of results, sorry.\n\nPlease Call 211 if you need more immediate assistance."


# Celery
# =======================================
CELERY_BROKER_URL = os.environ.get('CACHE_CELERY_LOCATION')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


# CORS 
# =======================================
if DEBUG:
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGIN_REGEXES = [r"^https?:\/\/.*"]
else:
    CORS_ALLOW_CREDENTIALS = True  
    CORS_ALLOWED_ORIGINS = [  
        f"https://{STREET_NINJA_WEBSITE_DOMAIN}",
        f"https://www.{STREET_NINJA_WEBSITE_DOMAIN}",
        f"https://{STREET_NINJA_API_DOMAIN}",
    ]  
    CSRF_TRUSTED_ORIGINS = [  
        f"https://{STREET_NINJA_WEBSITE_DOMAIN}", 
        f"https://www.{STREET_NINJA_WEBSITE_DOMAIN}",
        f"https://{STREET_NINJA_API_DOMAIN}",
    ]


# Geocoding
# =======================================
GEOCODER_CONFIG = {
    "NOMINATIM": {"user_agent": os.environ.get("NOMINATIM_USER_AGENT")},
    "OPENCAGE": {"api_key": os.environ.get("OPENCAGE_API_KEY")},
}
PRIMARY_GEOCODER = "Nominatim"  # Nominatim, OpenCage


# PHONE SESSION
# =======================================
TTL_PHONE_SESSION = int(os.environ.get("TTL_PHONE_SESSION", 3600))


# Routes
# =======================================
ROUTE_ADMIN = os.environ.get("ROUTE_ADMIN")
ROUTE_SMS_GATEWAY = os.environ.get("ROUTE_SMS_GATEWAY")


# Twilio
# =======================================
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")


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

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}


ROOT_URLCONF = 'street_ninja_server.urls'

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

WSGI_APPLICATION = 'street_ninja_server.wsgi.application'


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('CACHE_DEFAULT_LOCATION'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('CACHE_SESSION_LOCATION'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'phone_session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('CACHE_PHONE_SESSION_LOCATION'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'resources': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('CACHE_RESOURCES_LOCATION'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'celery': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('CACHE_CELERY_LOCATION'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'geo': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('CACHE_LOCATION_LOCATION'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'tests': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('CACHE_TESTS_LOCATION'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session'


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'TEST': {
            'NAME': 'test_street_ninja',
            'TEMPLATE': 'template_postgis',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
