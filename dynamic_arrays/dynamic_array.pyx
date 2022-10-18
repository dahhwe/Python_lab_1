# command: python setup.py build_ext --inplace

# cython: language_level=3
# distutils: language = c
# Указываем компилятору, что используется Python 3 и целевой формат
# языка Си (во что компилируем, поддерживается Си и C++)


# Также понадобятся функции управления памятью
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

# Для преобразования Python объекта float в Сишный тип и обратно
from cpython.float cimport PyFloat_AsDouble
from cpython.int cimport PyInt_AsLong

import sys

# Так как хотим использовать массив для разных типов, указывая только
# код типа без дополнительных заморочек, то используем самонаписанный
# дескриптор. Он будет хранить функции получения и записи значения в
# массив для нужных типов. Упрощенны аналог дескриптора из модуля array:
# https://github.com/python/cpython/blob/243b6c3b8fd3144450c477d99f01e31e7c3ebc0f/Modules/arraymodule.c#L32
cdef struct array_descr:
    # код типа, один символ
    char * typecode
    # размер одного элемента массива
    int item_size
    # функция получения элемента массива по индексу. Обратите внимание,
    # что она возвращает Python тип object. Вот так выглядит сигнатура на Си:
    # PyObject * (*getitem)(struct arrayobject *, Py_ssize_t)
    object (*getitem)(Array, size_t)
    # функция записи элемента массива по индексу. Третий аргумент это
    # записываемое значение, оно приходит из Python. Сигнатура на Си:
    # int (*setitem)(struct arrayobject *, Py_ssize_t, PyObject *)
    int (*setitem)(Array, size_t, array_object)

cdef object double_getitem(Array a, size_t index):
    """
    Функция получения значения из массива для типа double.
    Cython сам преобразует Сишное значение типа 
    double в аналогичны объект PyObject
    :param a: Массив  
    :param index: Индекс массива
    :return: значение из массива для типа double
    """
    return (<double *> a.data)[index]

cdef int double_setitem(Array a, size_t index, object obj):
    """
    Функция записи значения в массив для типа double. 
    :param a: Массив
    :param index: Индекс массива
    :param obj: Класс object()
    :return: флаг -1 при некорректном вводе
    """
    if not isinstance(obj, int) and not isinstance(obj, float):
        raise ValueError(
            'Элемент не является целочисленным числом или числом с'
            'плавающей запятой!')

    # Преобразования Python объекта в Сишный
    cdef double value = PyFloat_AsDouble(obj)

    if index >= 0:
        # Не забываем преобразовывать тип, т.к. a.data имеет тип char
        (<double *> a.data)[index] = value
    return 0

cdef object integer_getitem(Array a, size_t index):
    """
    Функция получения значения из массива для типа int.
    :param a: Массив
    :param index: Индекс Массива
    :return: значение из массива для типа int
    """
    return (<int *> a.data)[index]

cdef int integer_setitem(Array a, size_t index, object obj):
    """
    Функция записи значения в массив для типа int. 
    :param a: Массив
    :param index: Индекс Массива
    :param obj: Класс object()
    :return: флаг -1 при некорректном вводе
    """
    if not isinstance(obj, int) and not isinstance(obj, float):
        raise ValueError(
            'Элемент не является целочисленным числом или числом с'
            'плавающей запятой!')

    # Преобразования Python объекта в Сишный
    cdef int value = PyInt_AsLong(obj)

    if index >= 0:
        # Не забываем преобразовывать тип, т.к. a.data имеет тип char
        (<int *> a.data)[index] = value
    return 0

cdef array_descr[2] descriptors = [
    array_descr("d", sizeof(double), double_getitem, double_setitem),
    array_descr("i", sizeof(int), integer_getitem, integer_setitem)
    ]

cdef enum TypeCode:
    DOUBLE = 0
    INT = 1

cdef int char_typecode_to_int(str typecode):
    """
    Функция преобразовывает строковый код в число
    :param typecode: Строковый код
    :return: Преобразованное число
    """
    if typecode == "d":
        return TypeCode.DOUBLE
    elif typecode == "i":
        return TypeCode.INT
    return -1

cdef class Array:
    # Класс статического массива.
    # В поле length сохраняем длину массива, а в поле data будем хранить
    # данные. Обратите внимание, что для data используем тип char,
    # занимающий 1 байт. Далее мы будем выделять сразу несколько ячеек
    # этого типа для одного значения другого типа. Например, для
    # хранения одного double используем 8 ячеек для char.
    cdef public size_t length
    cdef public size_t allocated_length
    cdef char * data
    cdef array_descr * descr
    cdef str letter

    def __cinit__(self, str typecode, object num_array=None) -> None:
        """
        Аналог метода __init__
        :param typecode: Тип кода, int или double
        :param num_array: Массив
        :return:
        """
        if num_array is None:
            num_array = []

        self.length = self.allocated_length = len(num_array)
        cdef int m_typecode = char_typecode_to_int(typecode)
        self.descr = &descriptors[m_typecode]
        self.letter = typecode

        # Выделяем память для массива
        self.data = <char *> PyMem_Malloc(
            self.allocated_length * self.descr.item_size)

        if not self.data:
            raise MemoryError('Ошибка выделения памяти')

        for i in range(self.length):
            self.__setitem__(i, num_array[i])

    def append(self, object item) -> None:
        """
        Добавление элемента в массив
        :param item: элемент для добавления
        :return:
        """

        if self.valid_element(item):
            self.resize()
            self.length += 1
            self.__setitem__(self.length - 1, item)
        else:
            raise TypeError("Некорректное значение!")

    def valid_element(self, item):
        """
        Проверка значения на корректную форму
        :param item: Значение
        :return: Результат проверки
        """
        if (self.letter == 'i' and isinstance(item, int) or
            self.letter == 'd' and isinstance(item, float)) \
                and item <= sys.maxsize:
            return True
        return False

    def insert(self, object index, object value) -> None:
        """
        Операция вставки.
        :param index: Индекс массива
        :param value: объект для вставки
        :return:
        """
        if not isinstance(index, int):
            raise TypeError('Индекс не является целочисленным')

        if self.valid_element(value) and index < 0:
            if self.length + 1 <= abs(index):
                self.resize()
                self.length += 1

                for i in range(self.length - 1, 0, -1):
                    self.__setitem__(i, self.__getitem__(i - 1))

                self.__setitem__(0, value)

            elif -abs(self.length) <= index <= -1:
                self.resize()
                self.length += 1

                index = self.length - abs(index) - 1

                for i in range(self.length - 1, index, -1):
                    self.__setitem__(i, self.__getitem__(i - 1))

                self.__setitem__(index, value)

        elif index >= 0:
            if index >= self.length:
                self.resize()
                self.length += 1

                self.__setitem__(self.length - 1, value)

            elif 0 <= index <= self.length - 1:
                self.resize()
                self.length += 1

                for i in range(self.length - 1, index, -1):
                    self.__setitem__(i, self.__getitem__(i - 1))

                self.__setitem__(index, value)
        else:
            raise IndexError('Индекс не находится в пределах массива')

    def remove(self, object item) -> None:
        """
        Реализует операцию удаления элемента из массива.
        :param item: Элемент для удаления.
        :return:
        """
        cdef int i
        cdef int j

        for i in range(0, self.length):
            if self.__getitem__(i) == item:
                for j in range(i, self.length - 1):
                    self.__setitem__(j, self.__getitem__(j + 1))
                self.length -= 1
                break
            else:
                raise ValueError('Элемент отсутствует')

    def pop(self, int index=-1):
        """
        Реализует операцию удаления элемента из массива
        с возвратом значения.
        :param index: Индекс массива.
        :return: Удаленный элемент.
        """
        cdef int i
        cdef object number

        if index is None:
            index = -1
        if index < 0:
            index = self.length + index

        number = self.__getitem__(index)
        for i in range(index, self.length - 1):
            self.__setitem__(i, self.__getitem__(i + 1))
        self.length -= 1
        return number

    def resize(self) -> None:
        """
        Изменяет размерность массива.
        :return:
        """
        if self.length == self.allocated_length:
            self.allocated_length *= 2
            self.data = <char *> PyMem_Realloc(self.data,
                                               self.allocated_length * self.descr.item_size)

    def __str__(self) -> str:
        return str([i for i in self])  #super().__str__()

    def __repr__(self) -> str:
        return str([i for i in self])

    def __getitem__(self, object index) -> Array:
        """
        Получает элемент из массива по индексу.
        :param index: Индекс массива.
        :return: Ошибка индексации при получении некорректного значения индекса.
        """
        if isinstance(index, int):
            if 0 > index:
                index += self.length
            if index >= self.length or index < 0:
                raise IndexError('Индекс не находится в пределах массива!!!')
            else:
                return self.descr.getitem(self, index)
        else:
            raise TypeError('Индекс не является целочисленным')
    # Не забываем освобождать память. Привязываем это действие к объекту
    # Python. Это позволяет освободить память во время сборки мусора.

    def __setitem__(self, object index, object value) -> None:
        """
        Записывает элемента массива по индексу.
        :param index: Индекс массива.
        :param value: Записываемое значение
        :return:
        """
        if isinstance(index, int):
            if 0 > index:
                index = self.length + index
            if 0 <= index < self.length:
                self.descr.setitem(self, index, value)
            else:
                raise IndexError('Индекс не находится в пределах массива')
        else:
            raise TypeError('Индекс не является целочисленным')

    def __reversed__(self) -> Array:
        """
        "Переворачивает" все элементы массива.
        :return: Перевернутый массив.
        """
        cdef int i
        cdef object number
        for i in range(0, self.length // 2):
            number = self.__getitem__(self.length - 1 - i)
            self.__setitem__(self.length - 1 - i, self.__getitem__(i))
            self.__setitem__(i, number)
        return self

    def __len__(self) -> int:
        """
        Возвращает длину массива.
        :return: Длина массива.
        """
        return self.length

    def __sizeof__(self) -> int:
        """
        Возвращает количество памяти, выделенной под хранение
        элементов динамического массива (в байтах)
        :return:
        """
        return self.allocated_length * self.descr.item_size

    def __eq__(self, object other) -> bool:
        """
        Сравнивает динамический массив с другой коллекцией.
        :param other: другая коллекция.
        :return: True, если их длина и элементы идентичны
        Иначе возвращает False.
        """
        cdef int i
        for i in range(self.length):
            if self.__getitem__(i) == other[i]:
                return True
            return False

    def __dealloc__(self) -> None:
        """
        Очищает память.
        :return:
        """
        PyMem_Free(self.data)
