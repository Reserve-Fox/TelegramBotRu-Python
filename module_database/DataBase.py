__author__ = 'Reserve-Fox'
__version__ = 0.3

import os
import sqlite3

from DataBaseAPI import DataBaseAPI
from exception_classes import ConnectionFailed


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

    # -----------------------------------------------------------------
    def __init__(self, path_to_file: str, api: type[DataBaseAPI]) -> None:
        """
        Конструктор.

        Args:
            path_to_file (str): путь к файлу базы данных.
            api (type[DataBaseAPI]): класс представляющий API для БД.

        Raises:
            ConnectionFailed: Не удалось подключиться к БД.
        """
        self.__file_path: str = path_to_file
        
        # Проверка существования файла
        if not os.path.isfile(path=self.file_path):
            raise FileNotFoundError(f'Не удалось найти файл базы данных по пути: {self.file_path}')
        
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
            del connection


if __name__ == '__main__':
    db = DataBase(path_to_file='lkl', api=DataBaseAPI)
