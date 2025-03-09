import os
import logging
from logging.handlers import RotatingFileHandler


def configure_logging():
    """Configure application-wide logging with file rotation."""
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Create rotating file handler
    handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "app.log"),
        maxBytes=500 * 1024,  # 500KB
        backupCount=3,
    )

    # Set log format
    formatter = logging.Formatter("%(asctime)s|%(levelname)s|%(module)s|%(message)s")
    handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()

    # Only add handler if not already configured
    if not root_logger.handlers:
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.DEBUG)
