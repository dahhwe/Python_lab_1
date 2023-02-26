import concurrent.futures
from typing import Any, List, Optional, Tuple, Union

from PIL import Image

IMAGE_MAX_DEPTH = 8
ERROR_THRESHOLD = 13


class Point:
    """
    Класс точки в двумерном пространстве, заданную координатами x и y.
    """

    def __init__(self, x: float, y: float) -> None:
        """
        Конструктор
        :param x: Координата x.
        :param y: Координата y.
        """
        self.x = x
        self.y = y

    def __eq__(self, other: "Point") -> bool:
        """
        Сравнение двух точек.
        :param other: Точка для сравнения.
        :return: Результат сравнения.
        """
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        """
        :return: Cтроковое представление экземпляра класса.
        """
        return f"Point({self.x}, {self.y})"


def weighted_average(hist: List[int]) -> Tuple[Union[int, float], Union[int, float]]:
    """
    :param hist: Список целых чисел, представляющих гистограмму.
    :return: Кортеж из двух значений: средневзвешенное значение value и стандартное отклонение error.
    """
    total = sum(hist)
    if total == 0:
        return 0, 0
    value = sum(i * x for i, x in enumerate(hist)) / total
    error = sum(x * (i - value) ** 2 for i, x in enumerate(hist)) / total
    error = error ** 0.5
    return value, error


def color_from_histogram(hist: List[int]) -> Tuple[Tuple[int, int, int], Union[float, Any]]:
    """

    :param hist: Список целых чисел, представляющих гистограмму.
    :return: Кортеж из двух элементов: первый элемент - это кортеж с тремя целочисленными значениями от 0 до 255,
             представляющими красный, зеленый и синий каналы соответственно.
             Второй элемент - это число с плавающей точкой, представляющее ошибку,
             вычисленную на основе взвешенного среднего значений ошибок для каждого из каналов цвета.
    """
    red, red_error = weighted_average(hist[:256])
    green, green_error = weighted_average(hist[256:512])
    blue, blue_error = weighted_average(hist[512:768])
    error = red_error * 0.2989 + green_error * 0.5870 + blue_error * 0.1140
    return (int(red), int(green), int(blue)), error


class QuadtreeNode:
    """
    Представляет узел квадродерева, который содержит секцию изображения и информацию о ней.
    """

    def __init__(self, image: Image, border_box: tuple[int | Any, int | Any, Any, Any], depth: int) -> None:
        """
        Конструктор.
        """
        self.__border_box = border_box  # регион копирования
        self.__depth = depth
        self.__children = None
        self.__is_leaf = False

        # Обрезка части изображения по координатам
        image = image.crop(border_box)
        hist = image.histogram()
        self.__average_color, self.__error = color_from_histogram(hist)

    @property
    def depth(self) -> int:
        """
        :return: Возвращает глубину картинки.
        """
        return self.__depth

    @property
    def error(self) -> float:
        """
        :return: Возвращает полученную ошибку.
        """
        return self.__error

    @property
    def average_color(self) -> tuple[int, int, int]:
        """
        :return: Возвращает средний цвет.
        """
        return self.__average_color

    @property
    def children(self) -> Optional[list]:
        """
        :return: Возвращение дочерних узлов.
        """
        return self.__children

    @property
    def border_box(self) -> tuple[int | Any, int | Any, Any, Any]:
        """
        :return: Возвращает граничные точки.
        """
        return self.__border_box

    @property
    def is_leaf(self) -> bool:
        """
        :return: Возвращает сравнение квадранта с листом.
        """
        return self.__is_leaf

    @is_leaf.setter
    def is_leaf(self, value: bool) -> None:
        """
        :param value: Задает квадрант листом.
        :return:
        """
        self.__is_leaf = value

    def split(self, image: Image) -> None:
        """
        Разделяем картинку на 4 равные блока.
        :param image: Картинка.
        :return: None.
        """

        left, top, right, bottom = self.__border_box
        width, height = right - left, bottom - top

        if width <= 1 or height <= 1:
            return

        mid_x = (left + right) // 2
        mid_y = (top + bottom) // 2

        self.__children = [
            QuadtreeNode(image, (left, top, mid_x, mid_y), self.__depth + 1),
            QuadtreeNode(image, (mid_x, top, right, mid_y), self.__depth + 1),
            QuadtreeNode(image, (left, mid_y, mid_x, bottom), self.__depth + 1),
            QuadtreeNode(image, (mid_x, mid_y, right, bottom), self.__depth + 1)
        ]


class QuadTree:
    """
    Представляет четвертичное дерево, используемое для разбиения изображения на множество
    прямоугольников меньшего размера. Он использует рекурсивный алгоритм для деления изображения
    на подобласти до достижения максимальной глубины дерева или достижения минимальной ошибки.
    """

    def __init__(self, image: Image) -> None:
        """
        Конструктор.
        :param image: Картинка.
        """
        self.__width, self.__height = image.size
        self.__root = QuadtreeNode(image, image.getbbox(), 0)

        # keep track of max depth achieved by recursion
        self.__max_depth = 0
        self.__build_tree(image, self.__root)

    @property
    def width(self) -> int:
        """
        :return: Ширина картинки.
        """
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    def __build_tree(self, image: Image, node: QuadtreeNode) -> None:
        """
        Параллельный запуск задач с использованием ThreadPoolExecutor.
        Каждая задача запускается в отдельном потоке, и метод as_completed()
        используется для получения результатов по мере их завершения.
        :param image: Картинка.
        :param node:Узел.
        :return: None
        """
        if node.depth >= IMAGE_MAX_DEPTH or node.error <= ERROR_THRESHOLD:
            if node.depth > self.__max_depth:
                self.__max_depth = node.depth
            node.is_leaf = True
            return

        node.split(image)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for child in node.children:
                futures.append(executor.submit(self.__build_tree, image, child))

            for future in concurrent.futures.as_completed(futures):
                future.result()

        return None

    def get_leaf_nodes(self, depth: int) -> list:
        """
        Возвращает список всех листовых узлов дерева, которые находятся на заданной глубине.
        :param depth: Глубина.
        :return: Список всех листовых узлов дерева.
        """
        if depth > self.__max_depth:
            raise ValueError('Дана глубина больше, чем высота деревьев')

        def get_leaf_nodes_recursion(node, curr_depth):
            if curr_depth == depth or node.is_leaf:
                return [node]
            leaf_nodes = []
            for child in node.children:
                leaf_nodes.extend(get_leaf_nodes_recursion(child, curr_depth + 1))
            return leaf_nodes

        return get_leaf_nodes_recursion(self.__root, 0)
