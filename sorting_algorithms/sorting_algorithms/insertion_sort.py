import doctest


def insertion_sort(rand_list):
    """
    Сортировка массива вставками
    :param rand_list: рандомный массив
    :return sorted_list: отсортированный массив

    >>> insertion_sort([3,2,2,123,3,32,2,1,4,5,6,8])
    [1, 2, 2, 2, 3, 3, 4, 5, 6, 8, 32, 123]
    >>> insertion_sort([6,213,3,5,876,23,4,21,5,7,56])
    [3, 4, 5, 5, 6, 7, 21, 23, 56, 213, 876]
    """
    for index in range(1, len(rand_list)):
        current_value = rand_list[index]
        current_position = index
        while current_position > 0 and \
                rand_list[current_position - 1] > current_value:
            rand_list[current_position] = rand_list[current_position - 1]
            current_position = current_position - 1
        rand_list[current_position] = current_value
    sorted_list = rand_list
    return sorted_list


if __name__ == '__main__':
    doctest.testmod()
