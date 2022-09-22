"""
Класс с информацией о сотрудниках
"""


class Employee:
    """
    Инициализация атрибутов сотрудников
    """

    def __init__(self, first_name, last_name, workplace, position, salary):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__workplace = workplace
        self.__position = position
        self.__salary = salary
        self.__email = first_name+'.'+last_name+'@SuccessfulBusiness.co.uk'

    def show_data(self):
        """
        Вывод информации о сотрудниках
        :return:
        """
        print("Id\t\t:", self.__first_name)
        print("Name\t:", self.__last_name)
        print("Workplace\t:", self.__workplace)
        print("Position\t:", self.__position)
        print("Salary\t:", self.__salary)
