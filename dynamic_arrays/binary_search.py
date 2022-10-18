def search(sequence, item):
    low = 0
    high = len(sequence) - 1

    while low <= high:
        mid = (low + high) // 2

        if sequence[mid] < item:
            low = mid + 1
        elif sequence[mid] > item:
            high = mid - 1
        else:
            if mid - 1 < 0:
                return mid
            if sequence[mid - 1] != item:
                return mid
            high = mid - 1
