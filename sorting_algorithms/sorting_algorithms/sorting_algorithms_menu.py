import argparse
from random_list import get_rand_list
from bubble_sort import bubble_sort
from insertion_sort import insertion_sort
from merge_sort import merge_sort

sorting_methods = {'bubble_sort': bubble_sort,
                   'insertion_sort': insertion_sort,
                   'merge_sort': merge_sort}

parser = argparse.ArgumentParser(description='Sorting algorithms')
parser.add_argument('algorithm', choices=sorting_methods.keys(),
                    help='choose a sorting algorithm')
args = parser.parse_args()


def main():
    sorted_list = sorting_methods[args.algorithm]
    print(sorted_list)


if __name__ == "__main__":
    main()
