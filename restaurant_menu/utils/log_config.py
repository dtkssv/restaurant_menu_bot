import json
import logging
import os
import sys
import traceback
from logging import Handler, LogRecord, getLogger, handlers
from typing import Callable

from loguru import logger as loguru_logger

import restaurant_menu.core.config as config


class Formatter:
    """Формат для ведения журнала лога"""

    def __init__(
        self,
        app: str = "Бизнес тесты",
        service: str = "Business tests",
        version: str = os.getenv("VERSION", default="1.0.0"),
        oper_type: str = "LOG",
    ):
        """Внешние параметры для логирования
        Args:

        * app: Название функциональной подсистемы
        * service: Название микросервиса
        * version: Версия - Major.Minor.Fix-build
        * operType: тип
        """
        self.extra = {
            "app": app,
            "service": service,
            "version": version,
            "operType": oper_type,
        }

    def dev_format(self, record: dict) -> str:
        """Формат для консоли
        Args:

        * record: Информация о контексте ведения журнала
        """
        record["message"] = self.get_msg(record)

        fmt = (
            "<green>{time}</green> | "
            "<level>{level: <8}</level> {level.icon} | "
            "<cyan>{module}</cyan>:"
            "<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan> - "
            "{message}\n"
        )
        if record["exception"] and record["exception"].type is not None:
            fmt += "{exception}"

        return fmt

    def plaintext_format(self, record: dict) -> str:
        """Формат для консоли
        Args:

        * record: Информация о контексте ведения журнала
        """
        record["message"] = self.get_msg(record)
        fmt = (
            "{extra[app]} | "
            "{extra[service]} | "
            "{extra[version]} | "
            "{extra[operType]} | "
            "{level: <8} | "
            "{message: ^15} | "
            "{time:YYYY-MM-DDTHH:mm:ss.SSS[Z]}\n"
        )
        if record["exception"] and record["exception"].type is not None:
            fmt += "{exception}"

        return fmt

    def json_format(self, record: dict) -> str:
        """Формат для tcp -> строка формата json
        Args:

        * record: Информация о контексте ведения журнала
        """
        template = {
            "app": record["extra"]["app"],
            "service": record["extra"]["service"],
            "version": record["extra"]["version"],
            "operType": record["extra"]["operType"],
            "status": record["level"].name,
            "body": self.get_msg(record),
            "timestamp": f"{record['time']:%Y-%m-%dT%H:%M:%S.}{record['time'].microsecond // 1000}Z",
        }
        record["extra"]["serialize"] = json.dumps(template, ensure_ascii=False)

        return "{extra[serialize]}\n"

    @staticmethod
    def get_msg(record: dict) -> str:
        """Проверка ошибок в сообщении
        Args:

        * record: Информация о контексте ведения журнала
        """
        msg = record["message"]
        err = record["exception"]
        if err and err.type is not None:
            msg = f"{msg}: {traceback.format_exc()}"
        return msg


class InterceptHandler(Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class HandlerTCP(handlers.SocketHandler):
    def emit(self, record):
        try:
            self.send((self.format(record)).encode())
        except Exception:
            self.handleError(record)


def create_handler(
    sink, fmt: Callable, diagnose: bool, backtrace: bool, colorize: bool = True
) -> dict:
    handler = {
        "sink": sink,
        "colorize": colorize,
        "format": fmt,
        "diagnose": diagnose,
        "backtrace": backtrace,
    }
    return handler


def init_logger(formatter_: Formatter):
    """Инициализация лога с параметрами"""
    loguru_logger.remove()

    if config.settings.LOG_FORMAT == "dev":
        fmt = formatter_.dev_format
    else:
        fmt = formatter_.plaintext_format

    handler_console = create_handler(
        sys.stdout, fmt, config.settings.LOG_DIAGNOSE, config.settings.LOG_BACKTRACE
    )
    loguru_logger.configure(handlers=[handler_console], extra=formatter.extra)
    if config.settings.LOG_WRITER != "stdout":
        slice_host = slice(
            config.settings.LOG_WRITER.find("//") + 2, config.settings.LOG_WRITER.rfind(":")
        )
        slice_port = slice(config.settings.LOG_WRITER.rfind(":") + 1, None)
        host = config.settings.LOG_WRITER[slice_host]
        port = int(config.settings.LOG_WRITER[slice_port])
        handler_tcp = create_handler(
            HandlerTCP(host=host, port=port),
            formatter_.json_format,
            config.settings.LOG_DIAGNOSE,
            config.settings.LOG_BACKTRACE,
        )
        loguru_logger.add(**handler_tcp)

    # change handler for default uvicorn and fastapi logger
    getLogger("uvicorn.access").handlers = [InterceptHandler()]
    getLogger("uvicorn.error").handlers = [InterceptHandler()]

    return loguru_logger


formatter = Formatter()
log = init_logger(formatter)

if __name__ == "__main__":
    # Тестирование лога
    log.debug("Отладка - {level}", level="10")
    log.info("Информационное сообщение - 20")
    log.warning("Внимание! - 30")
    log.error("Ошибка! - 40")
    log.critical("Критическая ошибка! - 50")
    log.exception("Исключение")
