"""
Пакет отвечет за создание логгера телеграм бота.
"""

__author__ = 'Reverse-Fox'
__version__ = 1.0

__all__: list[str] = ['bot_logger']

from .logger import Logger, setup_logging_to_output
from .debug_logger import logger as debug_log
from .info_logger import logger as info_log
from .warning_logger import logger as warning_log
from .error_logger import logger as error_log
from .critical_logger import logger as critical_log

from typing import Tuple


if __name__ != '__main__':
    print(f'\nИмпортирован пакет {__name__} версии {__version__}\n')
    import logging

    # Список логгеров для присоединения
    loggers: Tuple[logging.Logger, ...] = (
        debug_log,
        info_log,
        warning_log,
        error_log,
        critical_log
    )

    # Форматтер сообщений
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(module)s - %(levelname)s - %(message)s'
    )

    # Настраиваем логгеры для вывода в терминал
    setup_logging_to_output(logger_list=loggers, formatter=formatter)

    # Привязка логгеров к единому объекту
    bot_logger = Logger(
        DEBUG=debug_log,
        INFO=info_log,
        WARNING=warning_log,
        ERROR=error_log,
        CRITICAL=critical_log
    )
