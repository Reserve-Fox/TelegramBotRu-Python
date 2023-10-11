__author__ = 'Reserve-Fox'
__version__ = 0.3

__all__: list[str] = ['DataBase']

import os
import sqlite3
from typing import Callable

from .DataBaseAPI import DataBaseAPI
from .exception_classes import ConnectionFailed


class DataBase:
    """
    Класс представляющий базу данных как объект с API для базы данных 
    как атрибут объекта.
    """
    @property
    def api(self) -> DataBaseAPI:
        return self.__api

    @property
    def file_path(self) -> str:
        return self.__file_path

    @property
    def output(self) -> Callable[..., None]:
        return self.__output

    # -----------------------------------------------------------------
    def __init__(self,
                 path_to_file: str,
                 api: type[DataBaseAPI],
                 output_func: Callable[..., None]) -> None:
        """
        Конструктор.

        Args:
            path_to_file (str): путь к файлу базы данных.
            api (type[DataBaseAPI]): класс представляющий API для БД.
            output_func (Callable[..., None]): функция для вывода при работе БД.

        Raises:
            ConnectionFailed: Не удалось подключиться к БД.
        """
        self.__file_path: str = path_to_file
        self.__output: Callable[..., None] = output_func

        # Проверка существования файла
        if not os.path.isfile(path=self.file_path):
            raise FileNotFoundError(
                f'Не удалось найти файл базы данных по пути: {self.file_path}'
            )

        # Подготовка API для базы данных
        try:
            connection: sqlite3.Connection = sqlite3.connect(
                database=self.file_path
            )
        except sqlite3.Error as error:
            raise ConnectionFailed(
                f'Не удалось установить соединение с файлом {self.file_path}', error
            )
        else:
            self.__api: DataBaseAPI = api(
                connection=connection
            )
            self.output(
                'Подключение к базе данных прошло успешно!'
                )

    # -----------------------------------------------------------------
    def __str__(self) -> str:
        return 'DB'

    # -----------------------------------------------------------------
    def __del__(self) -> None:
        self.api.disconnect()
        self.output(
            'Соединение с базой данных закрыто!'
            )


if __name__ != '__main__':
    print(f'----Импортирован модуль {__name__} версии {__version__}\n')