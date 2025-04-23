from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "ci-test-secret"
DEBUG = True
ALLOWED_HOSTS = ["*"]


EMAIL_HOST = ""
EMAIL_PORT = 55555
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True

EMAIL_ROUTE_CELERY = ""
EMAIL_ROUTE_DIRECTIONS = ""
EMAIL_ROUTE_LOCATION_PARSING = ""
EMAIL_ROUTE_LOGGING = ""
EMAIL_ROUTE_SENTRY = ""



# API Keys
# =======================================
VANCOUVER_OPEN_DATA_API_KEY = ""
WIGLE_API_KEY = ""
OPEN_ROUTE_SERVICE_TOKEN = ""
GRAPH_HOPPER_API_KEY = ""


# Domain
# =======================================
STREET_NINJA_WEBSITE_DOMAIN = ""
STREET_NINJA_API_DOMAIN = ""

SMS_CHAR_LIMIT = 400


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


# PHONE SESSION
# =======================================
TTL_PHONE_SESSION = 3600


# Routes
# =======================================
ROUTE_ADMIN = ""
ROUTE_SMS_GATEWAY = ""


# Twilio
# =======================================
TWILIO_AUTH_TOKEN = ""
TWILIO_ACCOUNT_SID = ""
TWILIO_PHONE_NUMBER = ""

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

# Add the bare minimum to boot Django
STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
