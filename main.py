"""
Программа, вычисляющая первых n-е обобщённое число
по ферме. Получает на вход числа (a, b и n),
выводит n-е число последовательности и
сообщения о делимости полученного числа.
"""
from typing import List


def input_check(num_char: str, limit: int) -> int:
    """
    input_check(num_char, limit)
    Проверяет, что на вход были получены именно числа
    заданного диапозона для (a, b и n).

    :param str num_char: относится к переменной,
                         для которой подбирается подходящее число

    :param int limit: лимит, меньше которого число не будет принято
    :return: int(value) возвращает подходящее число
    """
    while not (value := input(f"Введите число для {num_char} "
                              f"соответствующее ({limit} ≤ {num_char}):")) \
            or not value.isdigit() or int(value) < limit:
        print(f"Число должно быть больше или равно {limit}!")
    return int(value)


def quick_math() -> None:
    """
    quick_math()
    Получает раннее проверенные значения для (a, b и n),
    выполняет функцию и находит делители результата.
    Далее, выводит значение и делители.
    """
    value_a: int = input_check("a", 2)
    value_b: int = input_check("b", 1)
    value_n: int = input_check("n", 0)
    dividers: List[int] = []

    farm_n = value_a ** (2 ** value_n) + value_b ** (2 ** value_n)
    if not farm_n % 2:
        dividers.append(2)
    if not farm_n % 3:
        dividers.append(3)
    if not farm_n % 5:
        dividers.append(5)

    print()
    print(f"первых n-е обобщённое число: {farm_n}")
    if dividers:
        print(f"Число делится на: {dividers}")
    else:
        print("Число не делится на: 2, 3, 5")


def menu() -> None:
    """
    menu()
    Выводит графическое меню программы, с возможностью вычисления первого
     n-го обобщённого числа и выхода из нее
    """
    print("1. Вычислить n-е обобщённое число")
    print("3. Выйти из программы")


def main() -> None:
    """
    def main()
    main code function, this is where user gets to choose whether
    to start number calculation
    or to end the program.
    """
    menu()
    choice = input("Что вы хотите сделать: ")
    while choice != "3":
        if choice == "1":
            quick_math()
        else:
            print("Введите допустимое значение!")
        print()
        menu()
        choice = input("Что вы хотите сделать: ")
    print("До свидания!")


if __name__ == "__main__":
    main()
