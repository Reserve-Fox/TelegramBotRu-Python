import logging

from dataclasses import dataclass
from typing import List, Union, Tuple


@dataclass
class Logger:
    """
    Класс присоединяющий к себе логеры разных уровней.
    Используется для удобства доступа к логгированию на разных уровнях.
    """
    DEBUG: logging.Logger
    INFO: logging.Logger
    WARNING: logging.Logger
    ERROR: logging.Logger
    CRITICAL: logging.Logger


def setup_logging_to_output(
        logger_list: Union[List[logging.Logger], Tuple[logging.Logger, ...]],
        formatter: logging.Formatter) -> None:
    """
    Настраивает логгирование для вывода в консоль.
    """
    # Создаем обработчик логов для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=logging.DEBUG)

    # Устанавливаем форматтер для обработчика
    console_handler.setFormatter(fmt=formatter)

    # Настройка логгеров
    for logger in logger_list:
        logger.addHandler(hdlr=console_handler)
