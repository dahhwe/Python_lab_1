"""Основная программа"""

import argparse
import os
from typing import Any

from maze import make_maze, lee_algorithm, visualization_init
from read_files import reading_maze_from_text, \
    reading_maze_from_image


def validate_args(args: Any) -> bool:
    """Validate the command line arguments."""
    if args.width_height:
        if not 3 <= args.width_height[0] <= 500:
            print(f"Invalid width {args.width_height[0]}")
            return False
        if not 3 <= args.width_height[1] <= 500:
            print(f"Invalid height {args.width_height[1]}")
            return False

    if args.load_text:
        if not os.path.exists(args.load_text) or not args.load_text.endswith('.txt'):
            print("Invalid file")
            return False

    if args.load_image:
        if not os.path.exists(args.load_image) or not args.load_image.endswith(('.png', '.jpg')):
            print("Invalid file")
            return False
    return True


def parse_args() -> None:
    """Обработка параметров командной строки"""
    # Осуществляем разбор аргументов командной строки
    parser = argparse.ArgumentParser(description="Сжатие изображений на основе"
                                                 " квадродеревьев")

    # параметров командной строки
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-wh', '--width_height', nargs=2, dest="width_height",
                       type=int, help='Ширина и высота лабиринта (от 3 до 400)')

    group.add_argument('-limg', '--load-image', dest="load_image",
                       type=str,
                       help='Загрузка лабиринта из изображения')

    group.add_argument('-ltxt', '--load-text', dest="load_text",
                       type=str,
                       help='Загрузка лабиринта из текста')

    parser.add_argument("-sol", "--solution", dest="solution",
                        action="store_true", help="Решение лабиринта")

    parser.add_argument("-img", "--save-image", dest="save_image",
                        action="store_true", help="Сохранить лабиринт в виде изображения (jpg/png)")

    parser.add_argument("-txt", "--save-text", dest="save_text",
                        action="store_true", help="Сохранить лабиринт в виде текста (txt)")

    # В эту переменную попадает результат разбора аргументов командной строки.
    args = parser.parse_args()

    # Проверяем аргументы командной строки
    if validate_args(args):
        maze = [[]]

        if args.width_height:
            maze = make_maze(args.width_height[0], args.width_height[1])

        elif args.load_text:
            maze = reading_maze_from_text(args.load_text)

        elif args.load_image:
            maze = reading_maze_from_image(args.load_image)

        if args.solution:
            try:
                solution = lee_algorithm(maze)
                visualization_init(maze, solution, args.save_image,
                                   args.save_text)
            except (IndexError, KeyError):
                print("Ошибка выполнения. Завершение программы...")
        else:
            visualization_init(maze)
    else:
        print("Переданы неверные аргументы.")


def main():
    """Точка входа"""
    parse_args()


if __name__ == "__main__":
    main()
