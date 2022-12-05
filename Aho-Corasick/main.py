"""
Реализация алгоритма Ахо-Корасика, для поиска подстроки в строке
"""

import argparse
import os

from enum import Enum, unique, auto
from colorama import Fore
from search import search
from typing import Union


@unique
class StringFunc(Enum):
    """
    Нумератор для выбора действий меню
    """

    GET_USER_STR = auto()
    GET_USER_SUBSTR = auto()
    LOAD_STR_FROM_FILE = auto()
    FIND_MATCHES = auto()
    ADVANCED_MATCHES = auto()
    EXIT = auto()


def get_int_input() -> int:
    """
    Возвращает целочисленное число.
    :return: Целочисленное число
    """
    valid_input = False
    choice = input()
    while not valid_input:
        try:
            choice = int(choice)
        except ValueError:
            print("Введите число:")
            choice = input()
        else:
            valid_input = True
    return int(choice)


def get_user_input() -> str:
    """
    Возвращает введенную строку.
    :return: Введенная строка.
    """
    user_input = input("\nВведите строку (нажмите enter для отмены):")
    if not user_input:
        return ""
    return user_input


def print_menu() -> None:
    """
    Меню программы.
    :return:
    """
    print(
        """\n
    1 - Ввести строку
    2 - Ввести подстроку
    3 - Загрузить строку из файла
    4 - Поиск совпадений
    5 - Расширенный поиск совпадений
    6 - Выход
    """)


def started_parser() -> int:
    """
    Инициализация парсинга аргументов командной строки.
    :return: 0 - отсутствие аргументов, 1 - ошибка, 2 - значения приняты.
    """
    parser = argparse.ArgumentParser(description="collection of parameters")
    parser.add_argument("--str", type=str, help="user string")
    parser.add_argument("--file", type=str, help="file path")
    parser.add_argument("--substr", nargs="+", type=str, help="substring")
    parser.add_argument("--register", type=bool, help="case sensitive",
                        default=True)
    parser.add_argument("--method", type=str, help="searching method",
                        default="first")
    parser.add_argument(
        "--occurs", type=int, help="number of occurrences", default=None
    )
    args = parser.parse_args()
    parse = parse_arguments(args)
    return parse


def parse_arguments(args) -> int:
    """
    Получение и проверка аргументов командной строки.
    :param args: аргументы командной строки.
    :return: 0 - отсутствие аргументов, 1 - ошибка, 2 - значения приняты.
    """
    args_b = bool(args.str) + bool(args.file) + bool(args.substr)
    if not args_b:
        return False
    if not (args.str or args.file):
        print("Please, enter strings (--str) or a file name (--file)")
        print("Nowhere to search in")
        return True
    if args.file:
        if os.path.exists(args.file):
            string = load_str_from_file(args.file)
        else:
            print("This filename is incorrect")
            return True
    else:
        string = args.str
    if not args.substr:
        print("Please, enter keywords (--substr)")
        print("Nothing to search")
        return True
    substr = args.substr
    if isinstance(args.substr, list):
        substr = tuple(args.substr)
    case_sensitivity = args.register if args.register in (
        True, False) else False
    method = args.method if args.method in ("first", "last") else "first"
    count = args.occurs if args.occurs and args.occurs > 0 else None
    answer = search(string, substr, case_sensitivity, method, count)
    print_matches(string, answer, args.substr)
    return 2


def create_one_key(found: Union[tuple, None], key: str) -> list:
    """
    Создание массива индексов для одного ключа.
    :param found: индексы найденных ключевых слов.
    :param key: название искомого ключа.
    :return: массива индексов.
    """
    keys_ids = []

    for i, element in enumerate(found):
        keys_ids.append([])
        for j in range(len(key)):
            keys_ids[i].append(element + j)
    return keys_ids


def create_many_keys(found: Union[dict, None]) -> list:
    """
    Создание массива индексов для нескольких ключей.
    :param found: индексы найденных ключевых слов.
    :return: массива индексов.
    """
    keys_ids = []
    curr_id = -1

    for key, value in found.items():
        if value:
            for _, element in enumerate(value):
                keys_ids.append([])
                curr_id += 1
                for j in range(len(key)):
                    keys_ids[curr_id].append(element + j)
    return sorted(keys_ids)


def get_keys(found: Union[tuple, dict, None], key: str) -> list:
    """
    Создание массива индексов для одного или нескольких ключей.
    :param found: Индексы найденных ключевых слов.
    :param key: Название искомого ключа.
    :return: Массив индексов.
    """
    ids = []
    index = -1
    if isinstance(found, tuple):
        for i, element in enumerate(found):
            ids.append([])
            for j in range(len(key)):
                ids[i].append(element + j)
        return ids
    for dict_key, dict_val in found.items():
        if dict_val:
            for i, element in enumerate(dict_val):
                ids.append([])
                index += 1
                for j in range(len(dict_key)):
                    ids[index].append(element + j)
    return ids


def print_matches(
        string: str,
        substring: Union[tuple, str, None],
        matches_found: Union[tuple, dict, None]) -> None:
    """
    Вывод совпадений.
    :param string: Введенная строка.
    :param substring: Подстрока.
    :param matches_found: Найдены ли совпадения.
    :return:
    """
    colors = (
        Fore.LIGHTRED_EX,
        Fore.RED,
        Fore.LIGHTYELLOW_EX,
        Fore.YELLOW,
        Fore.LIGHTGREEN_EX,
        Fore.GREEN,
        Fore.LIGHTCYAN_EX,
        Fore.CYAN,
        Fore.LIGHTBLUE_EX,
        Fore.BLUE,
    )

    if not matches_found:
        print("Ничего не было найдено")
    else:
        matches_found = get_keys(matches_found, substring)
        first_match_index = 0
        for index, char in enumerate(string):
            if index > 389:
                break
            if index in matches_found[first_match_index]:
                print(f"{Fore.MAGENTA} {char}", end=" ")
            elif (
                    first_match_index < len(matches_found) - 1
                    and index in matches_found[first_match_index + 1]
            ):
                first_match_index += 1
                print(f"{colors[index % len(colors)]} {char}", end=" ")
            else:
                print(f"{Fore.RESET} {char}", end=" ")
            print(Fore.RESET, end=" ")


def advanced_search(
        user_str: str, user_substr: Union[tuple, str, None]
) -> Union[tuple, dict, None]:
    """
    Продвинутый поиск
    :param user_str: Строка
    :param user_substr: Подстрока
    :return: Результат продвинутого поиска подстроки в строке.
    """
    choices = ["да", "нет"]

    registry = input("Произвести поиск чувствительный к регистру? (Да / Нет):")
    while registry.lower() not in choices:
        registry = input(
            "Повторите ввод! Произвести поиск чувствительный " "к регистру? (Да / Нет):"
        )
    registry = registry.lower() == "да"

    print("Введите количество первых вхождений для поиска:")
    k_matches = get_int_input()
    while k_matches < 1:
        print(
            "Повторите ввод! Введите количество первых вхождений для поиска:")
        k_matches = get_int_input()

    check_direction = input("Произвести поиск с начала? (Да / Нет):")
    while check_direction.lower() not in choices:
        check_direction = input(
            "Повторите ввод! Произвести поиск с начала? (Да / Нет):"
        )
    if check_direction.lower() == "да":
        check_direction = "first"
    else:
        check_direction = "last"
    return search(user_str, user_substr, registry, check_direction)


def load_str_from_file(file_path=None) -> str:
    """
    Выгрузка строки из файла.
    :return: Выгруженная строка.
    """
    if not file_path:
        file_path = input("Введите путь к файлу:")
        while not file_path or not os.path.exists(file_path):
            file_path = input("Путь к файлу не найден, повторите ввод:")

    opened_file = open(file_path, "r")
    lines = opened_file.readlines()
    file_data = ""
    for i in lines:
        file_data = file_data + i

    opened_file.close()
    return file_data


def get_user_substr() -> tuple:
    """
    Возвращает подстроки.
    :return: Подстроки.
    """
    substring = []
    substr_item = ""

    while len(substring) < 1 or substr_item:
        substr_item = input("Введите подстроку (нажмите Enter для выхода): ")

        if substr_item in substring:
            print("Подстрока уже была добавлена")
        else:
            substring.append(substr_item)

    substring = filter(None, substring)
    return tuple(substring)


def main() -> None:
    """
    1 - Ввести строку
    2 - Ввести подстроку
    3 - Поиск совпадений
    4 - Загрузить строку из файла
    5 - Изменить конфигурацию поиска
    6 - Выход
    Главная функция программы, с возможностью дальнейшего выбора функций для
    реализации операций над матрицами.
    :return:
    """
    value = started_parser()
    if not value:
        command = ""
        string = None
        keywords = None

    print_menu()

    user_str = user_substr = ""
    print("Введите выбор:")
    choice = get_int_input()

    while choice != StringFunc.EXIT.value:
        if choice == StringFunc.GET_USER_STR.value:
            user_str = get_user_input()
            if user_str:
                print(f"Введенная строка: {user_str}")

        elif choice == StringFunc.GET_USER_SUBSTR.value:
            user_substr = get_user_substr()
            if user_substr:
                print(f"Введенная подстрока: {user_substr}")

        elif choice == StringFunc.FIND_MATCHES.value:
            result = search(user_str, user_substr)
            print_matches(user_str, user_substr, result)

        elif choice == StringFunc.LOAD_STR_FROM_FILE.value:
            user_str = load_str_from_file()
            print("Строка загружена")

        elif choice == StringFunc.ADVANCED_MATCHES.value:
            if user_substr and user_substr:
                result = advanced_search(user_str, user_substr)
                print_matches(user_str, user_substr, result)
            else:
                print("Строка или подстрока не заданы")

        else:
            print("Введите допустимое значение!")

        print_menu()
        print("Что вы хотите сделать?:")
        choice = get_int_input()
    print("До свидания!")


if __name__ == "__main__":
    main()
