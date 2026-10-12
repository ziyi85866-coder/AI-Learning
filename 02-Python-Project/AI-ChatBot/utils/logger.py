import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger():
    logger = logging.getLogger("AI-ChatBot")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    log_dir = Path(__file__).resolve().parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_dir / "chatbot.log",
        maxBytes=1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger