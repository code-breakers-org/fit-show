from .handler import env, BASE_DIR

LOGS_DIR = BASE_DIR / env.str("LOGS_DIR", "logs")
DEBUG_LOG_FILE = LOGS_DIR / env.str("DEBUG_LOG_FILENAME", "debug.log")

LOGGER_NAME = "FitShowLogger"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "\n\n"
                "DateTime: {asctime}\n"
                "Level: {levelname}\n"
                "FilePath: {pathname}\n"
                "Module: {module}\n"
                "Function: {funcName}\n"
                "Line: {lineno}\n"
                "Details: \n\t{message}\n"
            ),
            "style": "{",
        },
        "simple": {
            "format": "\n{levelname} {asctime} | {module} {funcName} => {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        LOGGER_NAME: {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": DEBUG_LOG_FILE,
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 250,
            "backupCount": 4,
        },
    },
    "loggers": {
        LOGGER_NAME: {
            "handlers": [LOGGER_NAME, "console"],
            "level": "DEBUG",
            "propagate": True,
        }
    },
}
