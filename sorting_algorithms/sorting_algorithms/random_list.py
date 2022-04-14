import random


def get_rand_list():
    """
    функция создаёт массив заданной длины заполненный случайными числами
    :return:
    """
    while not (list_size := input("Введите длину списка:")) \
            or not list_size.isdigit():
        print("Введите допустимую длину!")
    rnd_list = [random.randint(0, 9) for _ in range(int(list_size))]
    return rnd_list
