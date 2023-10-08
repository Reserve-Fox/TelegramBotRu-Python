"""
Тест для функции change_separators из модуля change_path_separators_on_os
"""

import unittest
import random
import string

from external_scripts.change_path_separators_on_os import change_separators as change_sep

from os.path import sep as os_sep
from typing import Dict, Union


class TestChangeSeparators(unittest.TestCase):
    @staticmethod
    def generate_test_data() -> Dict[str, str]:
        """
        Генерирует данные для теста.

        Returns:
            Dict[str, str]: old_separator, old_path
        """
        # Получаем случайный знак разделителя
        random_separator: str = random.choice(seq=string.punctuation)

        # Генерируем случайный путь для теста
        random_path: str = random_separator.join(
            [
                ''.join(
                    random.choices(
                        population=string.ascii_lowercase,
                        k=random.randint(a=1, b=10)
                    )
                )
                for _ in range(random.randint(a=4, b=10))
            ]
        )

        return {'old_separator': random_separator, 'old_path': random_path}

    def setUp(self) -> None:
        # Создаём словарь для теста
        self.data: Union[Dict[str, str], None] = self.generate_test_data()

        # Создаём контрольное значение для теста
        self.data['new_path'] = self.data['old_path'].replace(
            self.data['old_separator'],
            os_sep
        )

    def tearDown(self) -> None:
        self.data = None

    def test_function(self) -> None:
        # Получаем путь для теста
        self.data['test_path'] = change_sep(
            old_sep=self.data['old_separator'],
            path=self.data['old_path']
        )
        # Проводим тест
        self.assertEqual(
            first=self.data['test_path'],
            second=self.data['new_path'],
            msg=f'Тест не пройден!\nДанные тестовых значений:\n{self.data}'
        )

    def test_function_10_count(self) -> None:
        for _ in range(10):
            self.test_function()


if __name__ == '__main__':
    unittest.main()
