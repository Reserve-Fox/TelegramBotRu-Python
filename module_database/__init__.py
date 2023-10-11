# -*- coding: utf-8 -*-

"""
Модуль для установления соединения с базой данных SQLite
и предоставление API для взаимодействия с ней.
"""

__version__ = 0.4

__all__: list[str] = ['bot_database']

from external_scripts.get_bot_config import bot_config
from logger import bot_logger


if __name__ != '__main__':
    print(f'\nИмпортирован пакет {__name__} версии {__version__}')
    from .DataBase import DataBase
    from .DataBaseAPI import DataBaseAPI

    bot_database = DataBase(
        path_to_file=bot_config.DataBase['PathToFile'],
        api=DataBaseAPI,
        output_func=bot_logger.INFO.info
    )
