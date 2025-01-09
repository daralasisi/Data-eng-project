import logging
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# to move up one level to find data-eng-project/
PROJECT_ROOT = os.path.join(CURRENT_DIR, "..")

# combine that with "logs" to get `data-eng-project/logs`
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # this is to ensure that the logs folder exists

# constructing the full path to the log file
LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")

# 5. Set up the logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode='a'),
        logging.StreamHandler()
    ]
)

# Optional debug message to see that logging_config is loaded
logger = logging.getLogger(__name__)
logger.info("Logging configuration loaded. Logs will be stored in '%s'.", LOG_FILE_PATH)
