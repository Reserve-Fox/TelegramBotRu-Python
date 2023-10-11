# -*- coding: utf-8 -*-

"""
Главенствующий скрипт для запуска бота.
@Reserve-Fox
"""

__author__ = 'Reserve-Fox'
__version__ = 0.3

__all__: list[str] = [
    'bot_logger', 'bot_config', 'bot_database',
    'bot', 'dp'
]

import asyncio
import os
import importlib

from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, Router

from external_scripts import show_neko_terminal
from external_scripts.get_bot_config import bot_config
from logger import *
from module_database import bot_database

from typing import List, Dict
from types import ModuleType


# ---------------------------------------------------------------------
def get_routers_from_packages(path: str) -> Dict[str, Router]:
    """
    Подключает пакеты с функционалом для бота,
    используя main_router в __init__.py файлах.

    Args:
        path (str): путь к папке с пакетами.
    """
    # Ключ название пакета, значение основной роутер
    routers: Dict[str, Router] = {}

    # Получаем название пакетов в папке с функционалом бота
    # Игнорируем файлы с расширениями
    packages: List[str] = [
        package_name for package_name in os.listdir(path=path) if '.' not in package_name
    ]
    for package in packages:
        # Пытаемся получить пакет при помощи импорта
        try:
            module: ModuleType = importlib.import_module(
                name=f'{path}.{package}'
            )
        except ModuleNotFoundError as error:
            bot_logger.WARNING.warning(
                msg=f'Не удалось найти пакет {package}\n{error}'
            )
            continue
        # Достаём роутер из файла инициализации пакета
        router: Router = getattr(module, 'main_router')
        # Добавляем в словарь новый роутер
        routers[package] = router
    return routers


# ---------------------------------------------------------------------
def register_routers(routers: Dict[str, Router]) -> None:
    """
    Регистрирует роутеры с функционалом для бота в диспатчере.

    Args:
        routers (Dict[str, Router]): словарь с роутерами.
    """
    for router_name, router_object in routers.items():
        try:
            dp.include_router(router=router_object)
        except ValueError as error:
            bot_logger.WARNING.warning(
                msg=f'Не удалось подключить роутер {router_name}\n{error}'
            )


# ---------------------------------------------------------------------
bot = Bot(
    token=bot_config.Bot['Token'],
    parse_mode=ParseMode.HTML
)
dp = Dispatcher()


# ---------------------------------------------------------------------
async def main() -> None:
    """Основная функция для подготовки бота"""

    bot_logger.INFO.info(msg='Началось получение роутеров!')
    # Получаем роутеры с функционалом для бота
    routers: Dict[str, Router] = get_routers_from_packages(path='bot_modules')

    bot_logger.INFO.info(msg='Началась регистрация роутеров!')
    # Регистрируем роутеры
    register_routers(routers=routers)

    bot_logger.INFO.info(msg='Началась финальная подготовка бота!')
    # Отбрасываем все накопившиеся обновления
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# ---------------------------------------------------------------------
if __name__ == '__main__':
    from aiogram.exceptions import TelegramUnauthorizedError

    print('\n', '-'*79, end='\n\n') # Разделение вывода подготовки и запуска

    bot_logger.INFO.info(msg='Начался запуск бота!')
    try:
        asyncio.run(main=main())
    except KeyboardInterrupt:
        bot_logger.INFO.info(msg='Бот отключён!')
    except TelegramUnauthorizedError as error:
        bot_logger.CRITICAL.critical(
            msg=f'Токен бота не действителен!\n{error}'
        )
