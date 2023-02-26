"""
Основная программа для сжатия изображений на основе квадродеревьев. Содержит функции для проверки корректности
аргументов командной строки, парсинга аргументов и запуска сжатия изображения с указанными параметрами.
В основной функции main() происходит вызов функции parse_args() для парсинга аргументов и запуска сжатия.
Файл использует модуль argparse для парсинга аргументов командной строки, а также модуль os для проверки существования
исходного файла изображения. Кроме того, он использует функцию start_compression() из модуля image_compress для сжатия
изображения с помощью квадродеревьев.
"""

import argparse
import os
from typing import Union, Any

from image_compress import start_compression


def check_fields(args: Any) -> bool:
    """
    Проверка корректности аргументов.
    :param args: Аргументы.
    :return: True, при корректных аргументов.
    """

    if not os.path.exists(args.file):
        print(f"Ошибка: Файл {args.file} не найден.")
        return False

    # Check if the compression level is valid
    if args.level not in range(0, 9):
        print("Ошибка: Значение уровня сжатия должно быть от 0 до 8.")
        return False

    return True


def parse_args() -> Union[bool, str]:
    """
    Парс аргументов
    :return:
    """
    parser = argparse.ArgumentParser(description="Сжатие изображений на основе квадродеревьев")

    parser.add_argument("-f", "--file", dest="file", type=str,
                        help="Исходный файл изображения", required=True)

    parser.add_argument("-c", "--compress", dest="level", type=int,
                        help="Уровень сжатия", required=True)

    parser.add_argument("-s", "--show", dest="borders", action="store_true",
                        help="Отображение границ")

    parser.add_argument("-g", "--gif", dest="gif", action="store_true",
                        help="Создание gif-изображения")

    try:
        args = parser.parse_args()

        # Проверка корректности данных
        if check_fields(args):
            print(f"Сжатие уровня {args.level} запущено...")
            start_compression(args.file, args.level, args.borders, args.gif)
        else:
            print("Ошибка: Переданы неверные аргументы.")

    except argparse.ArgumentError as err:
        print(f"Ошибка: {err}")
        return False

    return True


def main() -> None:
    """
    Точка входа в программу
    """
    parse_args()


if __name__ == "__main__":
    main()
