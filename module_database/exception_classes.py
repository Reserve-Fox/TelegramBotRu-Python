# -*- coding: utf-8 -*-

"""
Модуль для авторских исключений пакета для работы с бд sqlite.

@Reserve-Fox
"""

__version__ = 0.1
__author__ = 'Reserve-Fox'

class ConnectionFailed(Exception):
    """
    Возбуждается когда не удалось подключиться к файлу базы данных.
    """

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)
