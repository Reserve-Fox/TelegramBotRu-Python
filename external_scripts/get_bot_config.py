"""
Данный скрипт предназначен для чтения .json файла конфигурации для бота.
Основная задача кода - отредактировать пути из конфига,
в пути текущей операционной системы, поскольку 
разделители путей в Linux и Windows различны.
"""

__author__ = 'Reverse-Fox'
__version__ = 1.0
__all__: list[str] = ['bot_config']

import json

from string import Template
from dataclasses import dataclass

from logger import bot_logger
from external_scripts.change_path_separators_on_os import change_separators

from typing import Dict, Union


# ---------------------------------------------------------------------
class ReadedJson(Dict[str, Dict[str, str]]):
    """
    Класс используемый для типизации в коде.
    Обозначает считанное содержимое JSON файла.
    """
    pass


# ---------------------------------------------------------------------
@dataclass
class BotConfig:
    """
    Класс используется для хранения данных из конфига.
    """
    Master: Dict[str, str]
    Bot: Dict[str, str]
    DataBase: Dict[str, str]
    Resources: Dict[str, str]
    Urls: Dict[str, str]

    def __str__(self) -> str:
        raw_template: Template = Template(template="""
Данные конфигурации бота:
    Master data: $master_data
    Bot data: $bot_data
    DataBase: $database_data
    Resources data: $resources_data
    Urls data: $urls_data
        """)

        template_data: Dict[str, Dict[str, str]] = {
            'master_data': self.Master,
            'bot_data': self.Bot,
            'database_data': self.DataBase,
            'resources_data': self.Resources,
            'urls_data': self.Urls,
        }

        return raw_template.safe_substitute(template_data)


# ---------------------------------------------------------------------
def get_json_config_data(path: str) -> ReadedJson:
    """
    get_json_config_data  считывает JSON файл.

    Args:
        path (str): путь к файлу конфигурации.

    Returns:
        ReadedJsonConfig: считанный JSON.
    """
    with open(file=path, mode='r') as json_file:
        config_data: ReadedJson = json.load(fp=json_file)

    return config_data


# ---------------------------------------------------------------------
def edit_json_config_paths_for_os(paths_data: ReadedJson, old_sep: str) -> None:
    """
    edit_json_config_paths_for_os заменяет старый разделитель
    путей в конфиге, на разделитель путей ОС.

    *Изменяет полученный конфиг, не возвращает новый!
    *Передавать словарь с путями

    Args:
        config (Dict[str, str]): конфиг для изменения.
        old_sep (str): разделитель путей в конфиге.
    """
    def replace_char_in_dict(
            data: Union[ReadedJson, Dict[str, str]],
            old_char: str) -> None:
        """
        Рекурсивная функция для замены разделителя в путях.

        В конфиге пути находятся в записи вида: 
            папка1: {путь1: path, путь2: path}
            папка2: {путь1: path, путь2: path}
        """
        for key, value in data.items():
            # Является ли значение словарём со строками
            if isinstance(value, dict):
                replace_char_in_dict(
                    data=value,
                    old_char=old_char
                )
            else:
                data[key] = change_separators(
                    old_sep=old_char,
                    path=value
                )

    # Замена разделителей
    replace_char_in_dict(
        data=paths_data,
        old_char=old_sep
    )


# ---------------------------------------------------------------------
def create_bot_config(config_data: ReadedJson) -> BotConfig:
    """
    create_bot_config наполняет dataclass данными из конфига.

    Args:
        config_data (ReadedJsonConfig): данные конфига.

    Returns:
        BotConfig: конфигурация для бота.
    """
    bot_configuration: BotConfig = BotConfig(
        Master=config_data['Master'],
        Bot=config_data['Bot'],
        DataBase=config_data['Paths']['DataBase'],
        Resources=config_data['Paths']['Resources'],
        Urls=config_data['Urls']
    )

    return bot_configuration


if __name__ != '__main__':
    print(f'Импортирован скрипт {__name__} версии {__version__}')

    # Получаем данные из файла конфигурации
    try:
        bot_config_json_data: ReadedJson = get_json_config_data(
            path='Bot_config.json'
        )
    except FileNotFoundError as error:
        bot_logger.CRITICAL.critical(
            msg=f"Файл конфигурации не найден! {error}"
        )
    except json.JSONDecodeError as error:
        bot_logger.CRITICAL.critical(
            msg=f"Ошибка декодирования JSON файла конфигурации! {error}"
        )

    # Редактируем пути в конфиге
    try:
        edit_json_config_paths_for_os(
            paths_data=bot_config_json_data['Paths'],
            old_sep='|'
        )
    except json.JSONDecodeError as error:
        bot_logger.CRITICAL.critical(
            msg=f"Ошибка изменения данных JSON файла! {error}"
        )

    # Завершение конфигурации для бота
    bot_config: BotConfig = create_bot_config(
        config_data=bot_config_json_data
    )
