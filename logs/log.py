import logging
from pathlib import Path

log_dir = Path(__file__).parent
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "app.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def log_info(message):
    logging.info(message)


def log_warning(message):
    logging.warning(message)


def log_error(message):
    logging.error(message)