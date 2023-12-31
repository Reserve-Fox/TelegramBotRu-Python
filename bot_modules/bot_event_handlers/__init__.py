# -*- coding: utf-8 -*-

__version__ = 1.0

__all__: list[str] = ['main_router']

from aiogram import Router

main_router = Router(name=__name__)

if __name__ != '__main__':
    print(f'\nИмпортирован пакет {__name__} версии {__version__}')
    from .bot_status_handlers import router as router1

    main_router.include_router(router=router1)
