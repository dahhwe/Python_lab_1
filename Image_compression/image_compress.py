"""
Файл содержит набор функций для сжатия изображений с использованием квадродерева.
Квадродерево представляет собой структуру данных, которая делит изображение на более мелкие квадраты
(называемые узлами), каждый из которых представляет собой либо один пиксель (если цвет пикселя внутри
квадрата одинаковый), либо средний цвет всех пикселей внутри квадрата (если цвета пикселей различны).
 Эта структура данных используется для уменьшения размера изображения без потери качества.
"""

import os
from typing import List

from PIL import Image, ImageDraw

from tree import QuadTree, IMAGE_MAX_DEPTH


class CreateGif:
    """
    Создание и сохранения Gif-изображений.
    """

    def __init__(self) -> None:
        """
        Конструктор класса
        """
        self.frames: List = []
        self.frames_count: int = 0
        self.gif_count: int = 1
        self.path: str = self.make_path()

    def make_path(self) -> str:
        """
        Метод создания пути к GIF.
        :return: Путь к GIF.
        """
        directory = "gifs"

        # If the .gif folder doesn't exist, create it
        if not os.path.exists(directory):
            os.mkdir(directory)

        path = os.path.join(directory, f"gif{self.gif_count}.gif")
        while os.path.exists(path):
            self.gif_count += 1
            path = os.path.join(directory, f"gif{self.gif_count}.gif")
        return path


def add_frame_to_gif(image: Image, gif: CreateGif) -> None:
    """
    Добавляет кадр к Gif.
    :param image: Кадр.
    :param gif: Экземпляр класса.
    :return:
    """
    try:
        gif.frames_count += 1
        gif.frames.append(image)
    except AttributeError:
        print("Ошибка: передан неверный объект для гиф-изображения.")
    except Exception as error_message:
        print(f"Произошла ошибка: {error_message}")


def save_gif(gif: CreateGif) -> None:
    """
    Cохраняет Gif в директорию.
    :param gif: Gif изображение
    :return:
    """
    if gif.frames_count == 0:
        print("Отмена. Нет кадров.")
        return

    try:
        gif.frames[0].save(gif.path, save_all=True, append_images=gif.frames[1:], optimize=True, duration=800, loop=0)
    except Exception as error_message:
        print(f"Ошибка при сохранении Gif: {error_message}")
        return

    print("Gif сохранена в директорию gifs")

    for frame in gif.frames:
        frame.close()

    gif.frames.clear()
    gif.frames_count = 0
    gif.gif_count += 1


def create_image(quadtree: QuadTree, level: int, borders: bool) -> Image:
    """
    Создает изображение на основе заданного квадродерева, уровня (level) и наличия границ (borders).
    :param quadtree: Квадродерево.
    :param level: Уровень дерева.
    :param borders: Границы.
    :return: Созданное изображение.
    """

    # Создает пустое изображение
    image = Image.new('RGB', (quadtree.width, quadtree.height))

    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, quadtree.width, quadtree.height), (0, 0, 0))

    # Получает список листовых узлов квадродерева, на заданном уровне
    leaf_nodes = quadtree.get_leaf_nodes(level)

    # Отрисовывает прямоугольники, соответствующие границам листовых узлов
    # на изображении, используя цвет усредненный из цветов всех пикселей в этом узле.
    # Если параметр borders равен True, то границы прямоугольников будут нарисованы черным цветом, а иначе без границ.
    for node in leaf_nodes:
        if borders:
            draw.rectangle(node.border_box, node.average_color,
                           outline=(0, 0, 0))
        else:
            draw.rectangle(node.border_box, node.average_color)

    return image


def start_compression(file: str, level: int, borders: bool, gif: bool) -> None:
    """
    Запускает процесс сжатия изображения с помощью квадродерева, и сохраняет результат в файл.
    :param file: Путь к файлу изображения, который должен быть сжат.
    :param level: Уровень сжатия изображения. Чем выше значение level, тем больше будет сжато изображение.
    :param borders: Определяет, следует ли рисовать границы листовых узлов квадродерева на сжатом изображении.
                    Если параметр равен True, то границы будут нарисованы черным цветом, а иначе без границ.
    :param gif: Булевое значение, определяющее, нужно ли создавать анимированный GIF-файл из нескольких сжатых
                изображений. Если параметр равен True, то будет создан GIF-файл.
                Если параметр равен False, то GIF-файл не будет создан.
    :return:
    """
    try:
        original_img = Image.open(file)
    except OSError:
        print(f"Ошибка: Не удалось открыть файл {file}")
        return

    quadtree = QuadTree(original_img)

    file_name, file_extension = os.path.splitext(file)

    result_image = create_image(quadtree, level, borders)
    result_image.save(f"{file_name}_compress_lvl_{level}{file_extension}")
    print("Изображение создано.")

    if gif:
        gif = CreateGif()

        for value in range(IMAGE_MAX_DEPTH + 1):
            new_img = create_image(quadtree, value, borders)
            add_frame_to_gif(new_img, gif)

        save_gif(gif)
        print("GIF-изображение создано.")
