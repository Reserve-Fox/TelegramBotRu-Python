import logging

from external_scripts.change_path_separators_on_os import change_separators as change_sep


# Создаем объект логгера
logger: logging.Logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.WARNING)

# Форматтер сообщений
formatter = logging.Formatter(
    fmt='%(asctime)s - %(module)s - %(message)s'
)

# Файл логгирования
file = logging.FileHandler(
    filename=change_sep(
        old_sep='|',
        path='Logs|warning.log'
    ),
    encoding='utf-8'
)
file.setLevel(level=logging.INFO)
file.setFormatter(fmt=formatter)

logger.addHandler(hdlr=file)
