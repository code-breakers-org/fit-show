from .env_handler import env

redis_host = env("REDIS_HOST")
redis_port = env("REDIS_PORT")
CELERY_BROKER_URL = f"redis://{redis_host}:{redis_port}"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
