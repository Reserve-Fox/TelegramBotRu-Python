__author__ = 'Reserve-Fox'
__version__ = 0.1

import sqlite3


class DataBaseAPI:
    """
    Класс представляющий API для работы с БД при помощи объекта.
    """
    @property
    def connection(self) -> sqlite3.Connection:
        return self.__connection

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.__connection: sqlite3.Connection = connection
