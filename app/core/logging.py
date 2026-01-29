import logging
import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("logs/app.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)
        return json.dumps(log_record)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_PATH)
        formatter = JsonFormatter()
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger