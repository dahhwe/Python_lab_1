"""
Класс с отделами работ
"""


class workplace:
    def __init__(self, name, address, location, requirements):
        """
        Инициализация атрибутов отделов
        """
        self.__name = name
        self.__address = address
        self.__location = location
        self.__requirements = requirements

    def workplace_information(self):
        """
        Вывод информации о отделах работ
        :return:
        """
        print("Name\t:", self.__name)
        print("Address\t\t:", self.__address)
        print("Location\t:", self.__location)
        print("Requirements\t:", self.__requirements)

    def list_data(self):
        return f'{self.__name} {self.__address} {self.__location} ' \
               f'{self.__requirements}'
