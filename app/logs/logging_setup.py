import json
import logging
import sys
from datetime import UTC, datetime
from logging.config import dictConfig

from app.core.settings import get_settings


class JsonFormatter(logging.Formatter):
    RESERVED_ATTRS = {
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "processName",
        "process",
        "asctime",
        "message",
    }

    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)

        # Корректно добавляем все extra-поля
        for key, value in record.__dict__.items():
            if key not in self.RESERVED_ATTRS:
                log[key] = value

        return json.dumps(log, ensure_ascii=False)


def setup_logging() -> None:
    settings = get_settings()
    is_prod = settings.env == "prod"

    formatters = {
        "default": {
            "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        },
        "json": {
            "()": JsonFormatter,
        },
    }

    handlers = {
        "default": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json" if is_prod else "default",
        },
    }

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": formatters,
            "handlers": handlers,
            "root": {
                "level": "WARNING",
                "handlers": ["default"],
            },
            "loggers": {
                # Приложение
                "app": {
                    "level": "INFO" if is_prod else "DEBUG",
                },
                # Uvicorn / Gunicorn
                "uvicorn.access": {
                    "level": "WARNING",
                    "propagate": False,
                },
                "uvicorn.error": {
                    "level": "INFO",
                    "propagate": False,
                },
                "gunicorn.access": {
                    "level": "WARNING",
                    "propagate": False,
                },
                "gunicorn.error": {
                    "level": "INFO",
                    "propagate": False,
                },
                # Asyncio
                "asyncio": {
                    "level": "WARNING",
                    "propagate": False,
                },
            },
        }
    )

    logging.getLogger("app").info(
        "Logging initialized",
        extra={"env": settings.env},
    )
