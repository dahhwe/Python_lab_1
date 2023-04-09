import os
import random
from collections import deque
from typing import Any, List, Dict, Tuple

import pygame as pg

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)


def ellers_algorithm(maze: list, height: int, width: int) -> list[list[str]] | Any:
    """
    Возвращает сгенерированный по алгоритму эйлера лабиринт.
    :param maze: Массив лабиринта.
    :param height: Высота лабиринта.
    :param width: Ширина лабиринта.
    :return: Построенный лабиринт.
    """
    row_set = [0] * width
    counter = 1
    random.seed()

    if width == 0:
        return [[" "]]

    if height <= 0 or width <= 0:
        raise ValueError("Height and width must be positive integers")

    # Aлгоритм Эйлера
    for i in range(height):
        for j in range(width):
            if row_set[j] == 0:
                row_set[j] = counter
                counter += 1
        for j in range(width - 1):
            right_wall = random.randint(0, 1)
            if right_wall == 1 or row_set[j] == row_set[j + 1]:
                maze[i * 2 + 1][j * 2 + 2] = "|"
            else:
                changing_set = row_set[j + 1]
                for _ in range(width):
                    if row_set[_] == changing_set:
                        row_set[_] = row_set[j]

        for j in range(width):
            down_wall = random.randint(0, 1)
            count_current_set = sum(row_set[_] == row_set[j] for _ in range(width))
            if down_wall == 1 and count_current_set != 1:
                maze[i * 2 + 2][j * 2 + 1] = "|"
        if i != height - 1:
            for j in range(width):
                count_hole = sum(
                    maze[i * 2 + 2][_ * 2 + 1] == " " and row_set[_] == row_set[j]
                    for _ in range(width)
                )
                if count_hole == 0:
                    maze[i * 2 + 2][j * 2 + 1] = " "
            for j in range(width):
                if maze[i * 2 + 2][j * 2 + 1] == "|":
                    row_set[j] = 0
    for j in range(width - 1):
        if row_set[j] != row_set[j + 1]:
            maze[-2][j * 2 + 2] = " "
    return maze


def make_maze(width: int, height: int) -> List[List[str]]:
    """
    Задает шаблон для генерации лабиринта.
    :param width: Ширина лабиринта.
    :param height: Высота лабиринта.
    :return: Сгенерированный лабиринт.
    """
    # Проверка отрицательных значений
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be non-negative")

    output_height = height * 2 + 1
    output_width = width * 2 + 1
    maze = [["|" for _ in range(output_width)] for _ in range(output_height)]

    for i in range(output_height):
        for j in range(output_width):
            if i % 2 == 1 and j % 2 == 1:
                maze[i][j] = " "
            elif i % 2 == 1 and j % 2 == 0 and j not in [0, output_width - 1]:
                maze[i][j] = " "
            elif j % 2 == 1 and i % 2 == 0 and i not in [0, output_height - 1]:
                maze[i][j] = " "
            else:
                maze[i][j] = "|"

    return ellers_algorithm(maze, height, width)


def lee_algorithm(maze: str) -> list[Any]:
    """
    Возвращает кратчайший путь решения лабиринта используя Алгоритм волнововой трассировки Ли.
    :param maze: Лабиринт.
    :return: Кратчайший путь.
    """
    # Установка точек входа и выхода лабиринта.
    entry = (1, 1)
    end_point = (len(maze) - 2, len(maze[0]) - 2)

    # Создание двусторонней очереди и добавление в нее точки входа.
    frontier = deque()
    frontier.append(entry)

    # Словарь для хранения путей.
    came_from = {entry: None}

    # Отслеживание посещенных точек.
    visited = set()

    while frontier:
        # Получает следующую точку из очереди.
        current = frontier.popleft()

        # При достижении конца, выход из цикла.
        if current == end_point:
            break

        # Получение соседних точек.
        for next_point in get_neighbors(current, maze):
            if next_point not in visited:
                # Добавление точки в queue.
                frontier.append(next_point)
                # Добавление пути к этой точке в словарь came_from.
                came_from[next_point] = current
                # Добавление точки к множеству посещенных точек.
                visited.add(next_point)

    # Реконструкция словаря came_from.
    try:
        return reconstruct_path(came_from, entry, end_point)
    except ValueError as error:
        print(error)
        return []


def get_neighbors(pos: Any, maze: str) -> list[tuple[int | Any, int | Any]]:
    """
    Возвращает список соседних точек для заданной позиции в лабиринте.
    :param pos: Кортеж из двух элементов, представляющий текущую позицию в лабиринте.
    :param maze: Строка, представляющая лабиринт.
    :return: Список кортежей из двух элементов, представляющих координаты соседних точек.
    """
    neighbors = []
    # Итерация по четырем направлениям: вверх, вниз, влево и вправо.
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        # Вычисление координат соседней точки
        neighbor_coordinates = (pos[0] + direction[0], pos[1] + direction[1])
        # Проверка того, что соседняя точка находится в пределах лабиринта.
        if 0 <= neighbor_coordinates[0] < len(maze) and 0 <= neighbor_coordinates[1] < len(maze[0]):
            # Проверка того, что соседняя точка не является стеной в лабиринте.
            if maze[neighbor_coordinates[0]][neighbor_coordinates[1]] != "|":
                # Добавление соседней точки в список соседей.
                neighbors.append(neighbor_coordinates)
    return neighbors


def reconstruct_path(
    frontier: Dict[Tuple[int, int], Tuple[int, int]],
    start: Tuple[int, int],
    end_point: Tuple[int, int],
) -> List[Tuple[int, int]]:
    """
    Функция восстанавливает путь от начальной точки до конечной точки в лабиринте.
    :param frontier: Словарь, содержащий информацию о том, какая точка была посещена перед текущей точкой.
    :param start: Кортеж из двух элементов, представляющий начальную точку в лабиринте.
    :param end_point: Кортеж из двух элементов, представляющий конечную точку в лабиринте.
    :return: Список кортежей из двух элементов, представляющих координаты точек на пути от начальной до конечной точки.
    """
    current = end_point
    path = []
    while current != start:
        path.append(current)
        if current not in frontier:
            raise ValueError("Path not found")
        current = frontier[current]
    path.append(start)
    path.reverse()
    return path


def print_maze(maze: List[List[str]]) -> None:
    """
    Функция выводит лабиринт в консоль.
    :param maze: Список списков строк, представляющий лабиринт.
    """
    if maze is None:
        return

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            print(maze[i][j], end="")
        print()


def visualize_maze(screen: pg.Surface, maze: List[List[str]], scale: int) -> None:
    """
    Функция визуализирует лабиринт на экране.
    :param screen: Экран pygame.
    :param maze: Список списков строк, представляющий лабиринт.
    :param scale: Масштаб отображения лабиринта.
    """
    if maze is None:
        return

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "|":
                pg.draw.rect(screen, BLACK, (j * scale, i * scale, scale, scale))
            else:
                pg.draw.rect(screen, WHITE, (j * scale, i * scale, scale, scale))

    pg.display.flip()


def init_pygame(maze: List[List[str]]) -> Tuple[pg.Surface, int]:
    """
    Функция инициализирует Pygame и создает окно для отображения лабиринта.
    :param maze: Список списков строк, представляющий лабиринт.
    :return: Кортеж из двух элементов: экран pygame и масштаб отображения лабиринта.
    """
    pg.init()
    width = len(maze[0])
    height = len(maze)

    scale = 1000 // height if height >= width else 1900 // width
    screen = pg.display.set_mode((width * scale, height * scale))
    return screen, scale


def show_solution(
    screen: pg.Surface,
    maze: List[List[str]],
    scale: int,
    solution: List[Tuple[int, int]] = None,
) -> None:
    """
    Функция визуализирует лабиринт и решение на экране.

    :param screen: Экран pygame.
    :param maze: Список списков строк, представляющий лабиринт.
    :param scale: Масштаб отображения лабиринта.
    :param solution: Список кортежей из двух элементов, представляющих координаты точек на пути от начальной до
    конечной точки.
    """
    visualize_maze(screen, maze, scale)

    if solution:
        show_path(screen, solution, scale)


def save_maze(
    screen: pg.Surface, maze: List[List[str]], image: bool = None, text: bool = None
) -> None:
    """
    Функция сохраняет изображение и текстовое представление лабиринта.
    :param screen: Экран pygame.
    :param maze: Список списков строк, представляющий лабиринт.
    :param image: Путь для сохранения изображения лабиринта.
    :param text: Путь для сохранения текстового представления лабиринта.
    """
    img_count = 1
    if image and os.path.exists("mazes"):
        existing_files = os.listdir("mazes")
        existing_images = [f for f in existing_files if f.endswith(".png")]
        img_count = len(existing_images) + 1

    if image:
        file_name = f"maze{img_count}.png"
        pg.image.save(screen, os.path.join("mazes", file_name))
        print(f"Изображение сохранено в 'mazes/{file_name}'")

    text_count = 1
    if text and os.path.exists("maze_text"):
        existing_files = os.listdir("maze_text")
        existing_text = [f for f in existing_files if f.endswith(".txt")]
        text_count = len(existing_text) + 1

    if text:
        file_name = f"maze{text_count}.txt"
        with open(os.path.join("maze_text", file_name), "w", encoding="utf-8") as file:
            for row in maze:
                file.write("".join(row) + "\r\n")
        print(f"Текст сохранен в 'maze_text/{file_name}'")


def visualization_init(
    maze: List[List[str]],
    solution: List[Tuple[int, int]] = None,
    save_image: bool = False,
    save_text: bool = False,
) -> None:
    """
    Функция инициализирует визуализацию лабиринта и решения.

    :param maze: Список списков строк, представляющий лабиринт.
    :param solution: Список кортежей из двух элементов, представляющих координаты точек на
    пути от начальной до конечной точки.
    :param save_image: Флаг, указывающий на необходимость сохранения изображения лабиринта.
    :param save_text: Флаг, указывающий на необходимость сохранения текстового представления лабиринта.
    """
    screen, scale = init_pygame(maze)
    show_solution(screen, maze, scale, solution)
    save_maze(screen, maze, save_image, save_text)

    solving = True
    while solving:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                solving = False


def show_path(screen: pg.Surface, solution: List[Tuple[int, int]], scale: int) -> None:
    """
    Функция визуализирует решение лабиринта на экране.

    :param screen: Экран pygame.
    :param solution: Список кортежей из двух элементов, представляющих координаты точек на пути от
    начальной до конечной точки.
    :param scale: Масштаб отображения лабиринта.
    """
    if solution is None:
        return

    color = pg.Color(0, 255, 0, 0)  # Начальный цвет.
    hue_step = 360 / len(solution)  # Расчет размера шага оттенка.

    for i, point in enumerate(solution):
        color.hsla = (i * hue_step, 100, 50, 100)  # Обновление значения оттенка.
        pg.draw.rect(screen, color, (point[1] * scale, point[0] * scale, scale, scale))
        pg.display.flip()
        pg.time.wait(30)
