"""
Написать функцию, реализующую алгоритм сортировки выбором.

Входные значения: список длиной n.
Выходные значения: отсортированный список длиной n.

"""
import random


def get_rand_list():
    """
    функция создает массив заданной длины заполненный случайными числами
    :return:
    """
    while not (list_size := input("Введите длину списка:")) \
            or not list_size.isdigit():
        print("Введите допустимую длину!")
    rand_list = [random.randint(0, 9) for _ in range(int(list_size))]
    return rand_list


def bubble_sort(rand_list):
    """
    сортировка массива методом bubble sort
    :param rand_list: рандомный массив
    :return:
    """
    list_length = len(rand_list)
    for i in range(list_length - 1):
        for j in range(0, list_length - i - 1):
            if rand_list[j] > rand_list[j + 1]:
                rand_list[j], rand_list[j + 1] = rand_list[j + 1], rand_list[j]


def insertion_sort(rand_list):
    """
    Сортировка массива вставками
    :param rand_list: рандомный массив
    :return:
    """
    for index in range(1, len(rand_list)):
        current_value = rand_list[index]
        current_position = index
        while current_position > 0 and \
                rand_list[current_position - 1] > current_value:
            rand_list[current_position] = rand_list[current_position - 1]
            current_position = current_position - 1
        rand_list[current_position] = current_value


def merge_sort(rand_list):
    """
    сортировка массива методом merge sort
    :param rand_list:
    :return:
    """
    if len(rand_list) > 1:
        mid = len(rand_list) // 2
        left = rand_list[:mid]
        right = rand_list[mid:]
        merge_sort(left)
        merge_sort(right)
        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                rand_list[k] = left[i]
                i += 1
            else:
                rand_list[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            rand_list[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            rand_list[k] = right[j]
            j += 1
            k += 1


def partition(array, begin, end):
    """
    часть метода сортировки quick sort
    :param array:
    :param begin:
    :param end:
    :return:
    """
    pivot = begin
    for i in range(begin + 1, end + 1):
        if array[i] <= array[begin]:
            pivot += 1
            array[i], array[pivot] = array[pivot], array[i]
    array[pivot], array[begin] = array[begin], array[pivot]
    return pivot


def quick_sort(array, begin=0, end=None):
    """
    метод сортироки quick sort
    :param array:
    :param begin:
    :param end:
    :return:
    """
    if end is None:
        end = len(array) - 1

    def quick_sort_part(list_to_sort, starting_pos, end_pos):
        if starting_pos >= end_pos:
            return
        pivot = partition(list_to_sort, starting_pos, end_pos)
        quick_sort_part(list_to_sort, starting_pos, pivot - 1)
        quick_sort_part(list_to_sort, pivot + 1, end_pos)
    return quick_sort_part(array, begin, end)


def invalid(array):
    """
    функция вызывается при неверном вводе для выбора метода сортировки чисел
    :param array:
    :return:
    """
    print(f"Некорректный ввод!, сгенерированный список: {array}")


def output_made_list(array):
    """
    Вывод сгенерированного списка
    :param array:
    :return:
    """
    print(f"сгенерированный список - {array}")


if __name__ == "__main__":
    random_list = get_rand_list()
    menu = {
        "1": ("Bubble sort", bubble_sort),
        "2": ("Insertion sort", insertion_sort),
        "3": ("Merge sort", merge_sort),
        "4": ("Quick sort", quick_sort),
        "5": ("Сгенерированный список", output_made_list),
        "6": ("Exit",)
    }

    while 1:
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        ans = input("Введите ваш выбор:")
        if ans != "6":
            menu.get(ans, [None, invalid])[1](random_list)
            if ans != "5":
                output_made_list(random_list)
        else:
            print("До свидания!")
            break
