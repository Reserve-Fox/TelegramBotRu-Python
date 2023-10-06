"""
Набор хэндлеров для статуса бота.

@Reserve-Fox
"""

__version__ = 1.0
__author__ = 'Reserve-Fox'

__all__: list[str] = ['router']

from aiogram import Router

from main import *


router = Router(name=__name__)


# ---------------------------------------------------------------------
@router.startup()
async def on_startup() -> None:
    """
    Уведомление об удачном запуске бота.
    """
    print('\nБот вышел в онлайн!')

    await bot.send_message(
        chat_id='-',
        text="<b>Я проснулась!</b>"
    )


# ---------------------------------------------------------------------
@router.shutdown()
async def on_shutdown() -> None:
    """
    Уведомление об выключении бота.
    """
    await bot.send_message(
        chat_id='-',
        text="<b>Я ухожу спать!</b>"
    )

    await bot.session.close()


if __name__ != '__main__':
    print(f'Импортирован модуль {__name__} версии {__version__}')
