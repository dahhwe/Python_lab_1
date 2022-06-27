"""1. Определить является ли заданная целочисленная квадратная матрица
магическим квадратом (магический квадрат – это квадратная матрица, у которой
суммы чисел в каждой строке, в каждом столбце и диагоналях равны между
собой).
2. Дана квадратная матрица порядка 2n. Получить новую матрицу,
переставляя ее блоки размера n x n крест-накрест. """

import numpy as np
from numpy import ndarray


def input_check(num_char: str, limit: int) -> int:
    """
    input_check(num_char, limit)
    Проверяет, что на вход было получено именно число
    заданного диапазона.
    :param str num_char: Фраза, относящаяся к переменной,
                         для которой подбирается подходящее число.
    :param int limit: Лимит, менее которого число не будет принято.
    :return: int(value) Подходящее число.
    """
    while not (value := input(f"Введите {num_char} ({limit} ≤ {num_char}):")) \
            or not value.lstrip('-').isdigit() or int(value) < limit:
        print(f"Число должно быть больше или равно {limit}!")
    return int(value)


def print_menu() -> None:
    """
    Меню программы.
    :return:
    """
    print("""\n
    1. Задать матрицу заполненную одинаковыми числами
    2. Задать матрицу заполненную случайными числами
    3. Проверить матрицу на магический квадрат
    4. Транспонировать матрицу
    5. Вывод матрицы
    6. Выход
    """)


def get_same_elem_matrix(matrix_size: int) -> ndarray:
    """
    Функция создает квадратную матрицу размера matrix_size наполненную
    одним числом.
    :param matrix_size: Размер матрицы.
    :return: list(matrix) Полученная матрица.
    """
    number = input_check("Число для матрицы", -10)
    matrix_to_make = np.full((matrix_size, matrix_size), number)
    return matrix_to_make


def get_matrix(matrix_size: int) -> ndarray:
    """
    Функция создает целочисленную квадратную матрицу размера matrix_size.
    :param matrix_size: Размер матрицы.
    :return: list(matrix) Полученная матрица.
    """
    matrix_to_make = np.random.randint(10, size=(matrix_size, matrix_size))
    return matrix_to_make


def magic_square(square_matrix):
    """
    Функция проверяет, является ли матрица магическим квадратом.
    :param square_matrix: Квадратная матрица.
    :return: При определении, что матрица - магический квадрат,
    возвращается значение True.
    """
    # Проверка размера
    for i in range(len(square_matrix)):
        if len(square_matrix[i]) != len(square_matrix):
            return False

    # Проверка строк
    for row in square_matrix:
        if sum(row) != sum(square_matrix[0]):
            return False

    # Проверка столбцов
    cols = [[row[column] for row in square_matrix] for
            column in range(len(square_matrix[0]))]
    for column in cols:
        if sum(column) != sum(square_matrix[0]):
            return False

    return True


def transpose_matrix(square_matrix: ndarray) -> ndarray:
    """
    Функция транспонирует матрицу (столбцы исходной матрицы
    становятся строками результирующей).
    :param square_matrix: Квадратная матрица.
    :return: транспонированная матрица.
    """
    t_matrix = square_matrix.T
    return t_matrix


def main() -> None:
    """
    Главная функция программы, с возможностью дальнейшего выбора функций для
    реализации операций над матрицами.
    :return:
    """
    print_menu()
    square_matrix = []

    choice = input("Что вы хотите сделать: ")
    while choice != "6":

        if choice == "1":
            matrix_size = input_check("Размер матрицы", 1)
            square_matrix = get_same_elem_matrix(matrix_size)
            print("Матрица задана!")

        elif choice == "2":
            matrix_size = input_check("Размер матрицы", 1)
            print(f"matrix size: {matrix_size}")
            square_matrix = get_matrix(matrix_size)
            print("Матрица задана!")

        elif choice == "3":
            print(f"Матрица является магическим квадратом!") if \
                len(square_matrix) and magic_square(square_matrix) \
                else print("Матрица не задана или"
                           " не является магическим квадратом")

        elif choice == "4":
            if len(square_matrix):
                square_matrix = transpose_matrix(square_matrix)
                print("Матрица транспонирована")
            else:
                print("Матрица не задана")

        elif choice == "5":
            print(square_matrix) if len(square_matrix) \
                else print("Матрица не задана")

        else:
            print("Введите допустимое значение!")

        print_menu()
        choice = input("Что вы хотите сделать: ")
    print("До свидания!")


if __name__ == "__main__":
    main()
