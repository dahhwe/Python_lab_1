"""
Реализация поиска подстроки по алгоритму Ахо-Корасика.
"""
import time
from builtins import object
from typing import Callable, Any


class Vertex:
    """
    Вершина Бора.
    """

    def __init__(self, identifier, symbol=None, parent=None,
                 success=False) -> None:
        """
        Инициализация вершины бора.
        :param identifier: Идентификатор.
        :param symbol: По какому символу из родителя пришли.
        :param parent: Родитель.
        :param success: Находится ли элемент в боре.
        """
        self.identifier = identifier
        self.longest_strict_suffix = None
        self.matched_keyword = None
        self.parent = parent
        self.symbol = symbol
        self.success = success
        self.transitions = {}


class Trie(object):
    """
    Бор
    """

    def __init__(self) -> None:
        """
        Инициализация бора.
        """
        self._root = Vertex(0)
        self._counter = 1
        self._final = False

    def add(self, keyword) -> None:
        """
        Добавляет ключевое слово к бору.
        :param keyword: Ключевое слово.
        :return:
        """
        if self._final:
            raise ValueError("Бор укомплектован. Невозможно добавить элементы")
        origin_word = keyword
        if len(keyword) < 1:
            return
        curr = self._root
        for char in keyword:
            try:
                curr = curr.transitions[char]
            except KeyError:
                next_state = Vertex(self._counter, parent=curr, symbol=char)
                self._counter += 1
                curr.transitions[char] = next_state
                curr = next_state
        curr.success = True
        curr.matched_keyword = origin_word

    def finalize(self) -> None:
        """
        Укомлектация бора. Выполняется после инициализации всех подстрок,
         перед началом поиска.
        :return:
        """
        if self._final:
            raise ValueError("Бор уже был укомплектован.")
        self._root.longest_strict_suffix = self._root
        self.search_lss_for_children(self._root)
        self._final = True

    def search_lss_for_children(self, zero_state) -> None:
        """
        Поиск потомков
        :param zero_state: изначальная позиция
        :return:
        """
        processed = set()
        to_process = [zero_state]
        while to_process:
            state = to_process.pop()
            processed.add(state.identifier)
            for child in state.transitions.values():
                if child.identifier not in processed:
                    self.search_lss(child)
                    to_process.append(child)

    def search_lss(self, state) -> None:
        """
        Поиск элементов
        :param state: Положение объекта
        :return:
        """
        zero_state = self._root
        parent = state.parent
        traversed = parent.longest_strict_suffix
        while True:
            if (
                    state.symbol in traversed.transitions
                    and traversed.transitions[state.symbol] is not state):
                state.longest_strict_suffix = traversed.transitions[
                    state.symbol]
                break
            if traversed is zero_state:
                state.longest_strict_suffix = zero_state
                break
            else:
                traversed = traversed.longest_strict_suffix
        suffix = state.longest_strict_suffix
        if suffix is zero_state:
            return
        if suffix.longest_strict_suffix is None:
            self.search_lss(suffix)
        for symbol, next_state in suffix.transitions.items():
            if symbol not in state.transitions:
                state.transitions[symbol] = next_state

    @property
    def root(self) -> Vertex:
        """
        Возвращает корень вершины бора.
        :return:
        """
        return self._root


def logger(func) -> Callable[[tuple[Any, ...], dict[str, Any]], Any]:
    """
    Логирует время работы функции и переданные ей аргументы.
    :param func: функция для логирования времени.
    :return:
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        results = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        print(f'Поиск подстрок завершен за {runtime:.3f} секунд')
        print(f'Аргументы: {args}, {kwargs}')
        return results

    return wrapper


@logger
def search(string, sub_string, case_sensitivity=False, method="first",
           count=None) -> None | tuple[int, ...] |\
        dict[tuple[Any, ...] | Any, list[Any] | None | Any]:
    """
    Поиск подстроки в строке методом Ахо-Корасика.
    :param string: Строка.
    :param sub_string: Подстрока.
    :param case_sensitivity: Чувствительность к регистру.
    :param method: Поиск с начала или с конца.
    :param count: Количество подстрок для нахождения.
    :return:
    """
    tree = Trie()
    if not case_sensitivity and string is not None:
        string = string.lower()
        if isinstance(sub_string, tuple):
            sub_string = list(sub_string)
            for i, n in enumerate(sub_string):
                n.lower()
            sub_string = tuple(sub_string)
        else:
            sub_string = sub_string.lower()
    if isinstance(sub_string, tuple):
        for item in sub_string:
            tree.add(item)
    else:
        tree.add(sub_string)
    tree.finalize()
    zero_state = tree.root
    current_state = zero_state
    found = {}
    if isinstance(sub_string, tuple):
        for item in sub_string:
            found[item] = []
    else:
        found[sub_string] = []
    items = []
    for idx, symbol in enumerate(string):
        current_state = current_state.transitions.get(
            symbol, zero_state.transitions.get(symbol, zero_state)
        )
        state = current_state
        while state is not zero_state:
            if state.success:
                keyword = state.matched_keyword
                idn = idx + 1 - len(keyword)
                items.append((keyword, idn))
            state = state.longest_strict_suffix
    if items:
        if method == "last":
            items = items[::-1]
        if count and len(items) > count:
            items = items[:count]
    else:
        return None
    if not isinstance(sub_string, tuple):
        t = []
        for i in items:
            t.append(i[1])
        return tuple(t)

    found = {}
    for char in sub_string:
        found[char] = []
    for i in items:
        found[i[0]].append(i[1])
    for key, value in found.items():
        if not value:
            found[key] = None
        else:
            found[key] = tuple(value)
    return found
