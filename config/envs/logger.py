from config.envs import env

LOGS_DIR_PATH = env.str("LOGS_DIR", "logs")
DEBUG_LOG_FILENAME = env.str("DEBUG_LOG_FILENAME", "debug.log")
