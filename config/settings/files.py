from .env_handler import env, BASE_DIR

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_DIR = BASE_DIR / "static"
STATIC_ROOT = env.str("PUBLIC_STATIC_ROOT", STATIC_DIR)

STATICFILES_DIRS = [BASE_DIR / "staticfiles"]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
MEDIA_DIR = BASE_DIR / "media_files"
MEDIA_ROOT = env.str("PUBLIC_MEDIA_ROOT", MEDIA_DIR)
MEDIA_URL = "/media/"

MAX_FILE_SIZE_MB = env.int("MAX_FILE_SIZE_MB", 5)

ACCEPTABLE_MEDIA_TYPE = ["png", "jpeg", "jpg"]
