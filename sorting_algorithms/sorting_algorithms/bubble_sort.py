import doctest


def bubble_sort(rand_list):
    """
    сортировка массива методом bubble sort
    :param rand_list: рандомный массив
    :return sorted_list: отсортированный массив

    >>> bubble_sort([5,2,12,5,2,5,1,0])
    [0, 1, 2, 2, 5, 5, 5, 12]
    >>> bubble_sort([9,8,1,2,6,7,3,13,31231231])
    [1, 2, 3, 6, 7, 8, 9, 13, 31231231]
    """
    list_length = len(rand_list)
    for i in range(list_length - 1):
        for j in range(0, list_length - i - 1):
            if rand_list[j] > rand_list[j + 1]:
                rand_list[j], rand_list[j + 1] = rand_list[j + 1], rand_list[j]
    sorted_list = rand_list
    return sorted_list


if __name__ == '__main__':
    doctest.testmod()
