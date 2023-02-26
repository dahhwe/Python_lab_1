"""
Дано два набора случайных целых чисел размером N и M
соответственно.
Предусмотреть:
• ввод границ и размеров для первого и второго наборов (могут
быть различны)
13
• вывод исходных наборов на экран
• вывод сначала количества, а затем отсортированные по
возрастанию числа такие, что каждое число есть в обоих наборах
• вывод количества и отсортированные по возрастанию остальные
числа в первом наборе
• вывод количества и отсортированные по возрастанию числа во
втором наборе
"""
import random


def get_list_size(name) -> int:
    """
    получить размерность для будущего списка
    :param name: название списка
    :return: размер списка
    """
    while not (list_size := input(f"Введите длину набора {name}:")) \
            or not list_size.isdigit():
        print("Введите допустимую длину!")
    return int(list_size)


def get_limit(name: str, phrase: str) -> int:
    """
    Получить допустимые границы для списка
    :param name: Название набора
    :param phrase: Номер предела
    :return: границы набора
    """
    while not (limit := input(f"Введите {phrase} предел "
                              f"для набора {name}:"))\
            or not limit.lstrip("-").isdigit():
        print("Введите допустимый предел!")
    return int(limit)


def get_list(list_name) -> list[int]:
    """
    Функция, создающая набор чисел наполненый
    случайными числами заданных размеров
    :param list_name: Название набора
    :return: random_list — набор наполненый случайными числами заданных
    размеров
    """
    list_size = get_list_size(list_name)
    limit_1 = get_limit(list_name, "Первый")
    limit_2 = get_limit(list_name, "Второй")
    if limit_1 > limit_2:
        lim_max = limit_1
        lim_min = limit_2
    else:
        lim_max = limit_2
        lim_min = limit_1
    print(f"{lim_min} — мин. предел, {lim_max} — макс. предел")
    random_list = [random.randint(lim_min, lim_max) for _ in range(list_size)]
    return random_list


def output_lists(rand_list_n: list, rand_list_m: list) -> None:
    """
    вывод наборов
    :param rand_list_n:
    :param rand_list_m:
    :return:
    """
    print(f"\033[96mN\033[0m {rand_list_n}")
    print(f"\033[96mM\033[0m {rand_list_m}")


def find_same_nums(rand_list_n: list, rand_list_m: list) -> None:
    """
    поиск одинаковых чисел в двух наборах и вывод этих чисел
    :param rand_list_n: набор N
    :param rand_list_m: набор M
    :return:
    """
    same_nums = []
    for i in rand_list_n:
        if i in set(rand_list_m):
            same_nums.append(i)
    same_nums.sort()
    if same_nums:
        print(f"Количество одинаковых чисел в наборах: {len(same_nums)}. "
              f"Эти числа: {same_nums}")
    else:
        print("одинаковых чисел в двух наборах нет")
    output_lists(rand_list_n, rand_list_m)


def other_nums_in_n(rand_list_n: list, rand_list_m: list) -> None:
    """
    Вывод остальных чисел из набора N
    :param rand_list_n:
    :param rand_list_m:
    :return:
    """
    same_nums = set(rand_list_n) & set(rand_list_m)
    other_nums = []
    for i in rand_list_n:
        if i not in same_nums:
            other_nums.append(i)
    rand_list_n.sort()
    if other_nums:
        print(f"Остальные числа: {other_nums}")
    else:
        print("Остальных чисел нет")
    print(f"набор N: {rand_list_n}")


def other_nums_in_m(rand_list_n: list, rand_list_m: list) -> None:
    """

    :param rand_list_n: набор N
    :param rand_list_m: набор M
    :return:
    """
    same_nums = set(rand_list_n) & set(rand_list_m)
    other_nums = []
    for i in rand_list_m:
        if i not in same_nums:
            other_nums.append(i)
    rand_list_m.sort()
    if other_nums:
        print(f"Остальные числа: {other_nums}")
    else:
        print("Остальных чисел нет")
    print(f"набор М: {rand_list_m}")


def print_menu() -> None:
    """
    menu()
    вывод графического меню программы
    """
    print("""
    1. Вывод исходных наборов
    2. Вывод количества и отсортированные по возврастанию числа,
    которые есть в N и M
    3. Вывод количества и отсортированные по возврастанию остальные
    числа из набора N 
    4. Вывод количества и отсортированные по возврастанию остальные
    числа из набора M
    5. Изменить наборы N и M 
    6. Выход
    """)


def main() -> None:
    """
    главная функция программы, с возможностью дальнейшего выбора функций для
    реализации заданных задач
    :return:
    """
    rand_list_n = get_list("N")
    rand_list_m = get_list("M")
    print_menu()
    choice = input("Что вы хотите сделать: ")
    while choice != "6":
        if choice == "1":
            output_lists(rand_list_n, rand_list_m)
        elif choice == "2":
            find_same_nums(rand_list_n, rand_list_m)
        elif choice == "3":
            other_nums_in_n(rand_list_n, rand_list_m)
        elif choice == "4":
            other_nums_in_m(rand_list_n, rand_list_m)
        elif choice == "5":
            rand_list_n = get_list("N")
            rand_list_m = get_list("M")
        else:
            print("Введите допустимое значение!")
        print_menu()
        choice = input("Что вы хотите сделать: ")
    print("До свидания!")


if __name__ == "__main__":
    main()
