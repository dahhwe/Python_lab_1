import pytest

from .. import bubble_sort
from .. import insertion_sort
from .. import merge_sort


def test_bubble_sort_empty_input():
    assert bubble_sort([]) == []


def test_insertion_sort_empty_input():
    assert insertion_sort([]) == []


def test_merge_sort_empty_input():
    assert merge_sort([]) == []


def test_bubble_sort_sorting():
    assert bubble_sort([6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6]


def test_insertion_sort_sorting():
    assert insertion_sort([9, 7, 5, 3, 2, 1]) == [1, 2, 3, 5, 7, 9]


def test_merge_sort_sorting():
    assert merge_sort([61, 25, 34, 13, 2, 1]) == [1, 2, 13, 25, 34, 61]


if __name__ == '__main__':
    pytest.main()
