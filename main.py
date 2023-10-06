# -*- coding: utf-8 -*-

"""
Главенствующий скрипт для запуска бота.
@Reserve-Fox
"""

__author__ = 'Reserve-Fox'
__version__ = 0.1

__all__: list[str] = ['bot_logger', 'bot', 'dp']

import asyncio
import os
import importlib

from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, Router

from external_scripts import show_neko_terminal
from logger import *

from typing import List, Dict
from types import ModuleType


# ---------------------------------------------------------------------
async def get_routers_from_packages(path: str) -> Dict[str, Router]:
    """
    Подключает пакеты с функционалом к боту,
    используя main_router в __init__.py файлах.

    Args:
        path (str): путь к папке с пакетами.
    """
    # Ключ название пакета, значение основной роутер
    routers_dict: Dict[str, Router] = {}

    # Получаем название пакетов в папке с функционалом бота
    packages: List[str] = [item for item in os.listdir(path=path) if '.' not in item]
    for package in packages:
        # Пытаемся получить модуль при помощи импорта
        try:
            module: ModuleType = importlib.import_module(name=f'{path}.{package}')
        except ModuleNotFoundError as error:
            print(f'Не удалось найти модуль {package}\n', error)
            continue
        # Достаём роутер из файла инициализации пакета
        router: Router = getattr(module, 'main_router')
        # Добавляем в словарь новый роутер
        routers_dict[package] = router
    return routers_dict


# ---------------------------------------------------------------------
async def register_routers(routers: Dict[str, Router]) -> None:
    """
    Регистрирует роутеры с функционалом для бота в диспатчере.

    Args:
        routers (Dict[str, Router]): словарь с роутерами.
    """
    for router_name, router in routers.items():
        try:
            dp.include_router(router=router)
        except ValueError as error:
            print(f'Не удалось подключить роутер {router_name}\n', error)


# ---------------------------------------------------------------------
bot = Bot(
    token='-',
    parse_mode=ParseMode.HTML
)
dp = Dispatcher()


# ---------------------------------------------------------------------
async def main() -> None:
    """Основная функция для подготовки бота"""
    # Получаем роутеры с функционлаом бота
    routers: Dict[str, Router] = await get_routers_from_packages(path='bot_modules')

    # Регистрируем роутеры
    await register_routers(routers=routers)

    # Отбрасываем все накопившиеся обновления
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# ---------------------------------------------------------------------
if __name__ == '__main__':
    from aiogram.exceptions import TelegramUnauthorizedError

    try:
        asyncio.run(main=main())
    except KeyboardInterrupt:
        print(
            'Бот отключён!'
        )
    except TelegramUnauthorizedError as error:
        print(
            'Токен бота не действительный!', error, sep='\n'
        )
