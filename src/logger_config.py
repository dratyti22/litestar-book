from litestar.logging import LoggingConfig

logging_config = LoggingConfig(
    root={"level": "DEBUG", "handlers": ["console"]},
    formatters={
        "default": {
            "format": "[%(asctime)s] - #%(levelname)-8s %(pathname)s - %(funcName)s - line: %(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    loggers={
        "litestar": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "sqlalchemy": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        "auth": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "uvicorn.error": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "uvicorn.access": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        "src": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
    },
)