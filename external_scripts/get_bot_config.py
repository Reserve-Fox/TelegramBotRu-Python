"""
Данный скрипт предназначен для чтения .json файла конфигурации для бота.
"""

__version__ = 1.0
__all__: list[str] = ['bot_config']

import json

from os.path import sep as os_separator
from string import Template
from dataclasses import dataclass

from logger import bot_logger

from typing import Dict, Union


class ReadedJsonConfig(Dict[str, Dict[str, str]]):
    """
    Класс используемый для типизации в коде.
    Обозначает считанное содержимое JSON файла.
    """
    pass


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
Мнформация из конфига для бота:
    Master data: $master_data
    Bot data: $bot_data
    DataBase: $database_data
    Resources data: $resources_data
    Urls data: $urls_data
        """)

        data_dict: Dict[str, Dict[str, str]] = {
            'master_data': self.Master,
            'bot_data': self.Bot,
            'database_data': self.DataBase,
            'resources_data': self.Resources,
            'urls_data': self.Urls,
        }

        return raw_template.safe_substitute(data_dict)


def get_json_config_data(path: str) -> ReadedJsonConfig:
    """
    get_json_config_data  считывает JSON файл.

    Args:
        path (str): путь к файлу конфигурации.

    Returns:
        ReadedJsonConfig: считанный JSON.
    """
    with open(file=path, mode='r') as file:
        config_data: ReadedJsonConfig = json.load(fp=file)

    return config_data


def edit_json_config_paths_for_os(config: ReadedJsonConfig, old_sep: str) -> ReadedJsonConfig:
    """
    edit_json_config_paths_for_os заменяет старый разделитель
    в путях конфига, на разделитель путей ОС

    Args:
        config (ReadedJsonConfig): считаный конфиг.
        old_sep (str): разделитель путей в конфиге.

    Returns:
        ReadedJsonConfig: изменённый конфиг.
    """
    def replace_char_in_dict(
            dict_: Dict[str, Union[str, Dict[str, str]]],
            old_char: str,
            new_char: str) -> None:
        """
        Рекурсивная функция для замены разделителя.
        """
        for key, value in dict_.items():
            # Является ли значение словарём со строками
            if isinstance(value, dict):
                replace_char_in_dict(
                    dict_=value,
                    old_char=old_char,
                    new_char=new_char
                )
            else:
                dict_[key] = value.replace(old_char, new_char)

    # Замена разделителей
    replace_char_in_dict(
        dict_=config, old_char=old_sep, new_char=os_separator
    )

    return config


def create_bot_config(config_data: ReadedJsonConfig) -> BotConfig:
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
        DataBase=config_data['DataBase'],
        Resources=config_data['Resources'],
        Urls=config_data['Urls']
    )

    return bot_configuration


if __name__ != '__main__':
    print(f'Импортирован модуль {__name__} версии {__version__}\n')

    # Получаем данные из файла конфигурации
    try:
        TBotConfig: ReadedJsonConfig = get_json_config_data(
            path='Bot_config.json')
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
        new_config_data: ReadedJsonConfig = edit_json_config_paths_for_os(
            config=TBotConfig,
            old_sep='|'
        )
    except json.JSONDecodeError as error:
        bot_logger.CRITICAL.critical(
            msg=f"Ошибка изменения данных JSON файла! {error}"
        )

    # Завершение конфигурации для бота
    bot_config: BotConfig = create_bot_config(
        config_data=new_config_data
    )
