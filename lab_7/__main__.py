"""Разработайте программу для хранения данных о сотрудниках в
организации.
Организация состоит из нескольких отделов, в каждом из которых
работают несколько сотрудников на разных должностях.

Разработайте и реализуйте диаграмму классов и все необходимые
методы, и свойства."""
from employees import Employee
from workplace import workplace

LIST_EMPLOYEES = []
WORKPLACES = []


def output_employees():
    """
    Вывод сотрудников с помощью класса
    :return:
    """
    for i, val in enumerate(LIST_EMPLOYEES):
        print(i+1)
        Employee.show_data(LIST_EMPLOYEES[i])
        print()


def get_employees_list():
    """
    Получен список сотрудников
    :return:
    """
    emp_1 = Employee('Tyler', 'Joseph', 'office', 'manager', '50000')
    emp_2 = Employee('Seamus', 'Smith', 'technical center', 'engineer', '4200')
    emp_3 = Employee('Isac', 'Nel', 'store', 'salesman', '20000')
    LIST_EMPLOYEES.append(emp_1)
    LIST_EMPLOYEES.append(emp_2)
    LIST_EMPLOYEES.append(emp_3)


def add_employee():
    """
    Функция добавляет нового сотрудника в список LIST_EMPLOYEES
    :return:
    """
    employee_id = input("Enter Employers id:\t")
    first_name = input("Enter First Name:\t")
    last_name = input("Enter Last Name:\t")
    place_of_work = input("Enter Workplace:\t")
    position = input("Enter Position:\t")
    salary = int(input("Enter Salary:\t"))
    employee_id = Employee(first_name, last_name, place_of_work, position,
                           salary)
    LIST_EMPLOYEES.append(employee_id)


def invalid():
    """
    Функция вызвана при некорректном вводе в меню
    :return:
    """
    print("Enter a valid input!")


def delete_employee():
    """
    Функция удаляет данные о рабочем
    :return:
    """
    output_employees()
    while not (slave_num := input("Enter a keyword:\t")) or\
            slave_num.isalpha():
        print('Enter a valid input!')
    LIST_EMPLOYEES.pop(int(slave_num)-1)
    print(f'removed {slave_num}')


def get_workplace_list():
    """
    Функция получает информацию о местах работы
    :return:
    """
    workplace_1 = workplace('Headquaters', 'Baker st. 221b', 'Russia', 'lvl5')
    workplace_2 = workplace('Research dev.', 'Gleneagles ave 10', 'Russia',
                            '3 years experience')
    workplace_3 = workplace('Shop', 'epidemic ave 54', 'Russia',
                            'sales skills')
    WORKPLACES.append(workplace_1)
    WORKPLACES.append(workplace_2)
    WORKPLACES.append(workplace_3)


def output_workplace():
    """
    Функция выводит места работ
    :return:
    """
    for i, item in enumerate(WORKPLACES):
        workplace.workplace_information(item)
        print()


def main():
    """
    Функция включает в себя графическое меню программы оформленное с помощью
    словаря, и дальнейшим выбором функция для работы с ней.
    :return:
    """
    menu = {
        "1": ("Вывести информацию о сотрудниках", output_employees),
        "2": ("Добавить сотрудника", add_employee),
        "3": ("Удалить сотрудника", delete_employee),
        "4": ("Вывести информацию о отделах", output_workplace),
        "5": ("Exit",)
    }
    get_employees_list()
    get_workplace_list()
    while 1:
        for key in sorted(menu.keys()):
            print(key+":"+menu[key][0])
        ans = input("Введите ваш выбор:")
        if ans != "5":
            menu.get(ans, [None, invalid])[1]()
        else:
            print("До свидания!")
            break


if __name__ == "__main__":
    main()
