__author__ = 'Reserve-Fox'
__version__ = 0.1

__all__: list[str] = ['DataBaseAPI']

import sqlite3


class DataBaseAPI:
    """
    Класс представляющий API для работы с БД при помощи объекта.
    """
    @property
    def connection(self) -> sqlite3.Connection:
        return self.__connection

    # -----------------------------------------------------------------
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.__connection: sqlite3.Connection = connection

    # -----------------------------------------------------------------
    def disconnect(self) -> None:
        self.connection.close()


if __name__ != '__main__':
    print(f'----Импортирован модуль {__name__} версии {__version__}')
