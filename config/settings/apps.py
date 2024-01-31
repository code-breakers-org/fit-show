import os
import sys

from .handler import BASE_DIR

# Define the 'apps' directory path
APPS_DIR = os.path.join(BASE_DIR, "apps")
sys.path.insert(0, APPS_DIR)

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = ["core", "user"]

# CHECK IF INSTALLED APPS INCLUDE THE PACKAGE FIRST
THIRD_PARTY_APPS = [
    "phonenumber_field",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework_simplejwt",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
