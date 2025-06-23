import django
import os


def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "street_ninja_server.settings")
    django.setup()
