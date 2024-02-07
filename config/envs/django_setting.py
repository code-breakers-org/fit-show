from config.envs.handler import env

SECRET_KEY = env.str(
    "SECRET_KEY",
    default="django-insecure-^hx4vco_&p3urjr5p9y1evw7^p%caba0+3p64q=a$!2l&=z=oz",
)


ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])


TIME_ZONE = env.str("TIMEZONE", default="UTC")
