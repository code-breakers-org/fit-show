from config.environment_variables import PUBLIC_STATIC_ROOT, PUBLIC_MEDIA_ROOT, BASE_DIR


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

STATIC_ROOT = PUBLIC_STATIC_ROOT

STATICFILES_DIRS = [BASE_DIR / "staticfiles"]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
MEDIA_ROOT = PUBLIC_MEDIA_ROOT
MEDIA_URL = "/media/"
