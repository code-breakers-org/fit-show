from config.envs import LOGS_DIR_PATH, DEBUG_LOG_FILENAME, BASE_DIR

LOGS_DIR = BASE_DIR / LOGS_DIR_PATH
DEBUG_LOG_FILE = LOGS_DIR / DEBUG_LOG_FILENAME

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
