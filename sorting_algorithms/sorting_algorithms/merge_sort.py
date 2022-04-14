import doctest


def merge_sort(rand_list):
    """
    сортировка массива методом merge sort
    :param rand_list: рандомный массив
    :return sorted_list: отсортированный массив

    >>> merge_sort([23,321,0,32,123,534,234,123,923])
    [0, 23, 32, 123, 123, 234, 321, 534, 923]
    >>> merge_sort([2,9,9,23,3212,3,42,4919,223,2,3])
    [2, 2, 3, 3, 9, 9, 23, 42, 223, 3212, 4919]
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
    sorted_list = rand_list
    return sorted_list


if __name__ == '__main__':
    doctest.testmod()
