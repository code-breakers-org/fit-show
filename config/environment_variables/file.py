from config.environment_variables.handler import env, BASE_DIR


STATIC_DIR = BASE_DIR / "static"
# This ENV variable will be used in the CI/CD
PUBLIC_STATIC_ROOT = env.str("PUBLIC_STATIC_ROOT", STATIC_DIR)

# This ENV variable will be used in the CI/CD
MEDIA_DIR = BASE_DIR / "media"
PUBLIC_MEDIA_ROOT = env.str("PUBLIC_MEDIA_ROOT", MEDIA_DIR)
