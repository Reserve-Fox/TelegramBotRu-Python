import logging

# Создаем объект логгера
logger: logging.Logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.ERROR)