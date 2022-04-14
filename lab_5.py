"""
Написать программу, реализующую хранение информации об ВУЗах.
Структура: наименование, год открытия, количество факультетов,
количество студентов.
Программа должна позволять:
а) загружать информацию из файла;
б) выполнять поиск товара по наименованию;
в) фильтровать товары по количеству студентов;
г) добавлять записи;
д) удалять записи;
е) сохранять данные в файле.
Для выполнения задания используйте стандартный модуль csv.
"""
import csv
from _csv import writer


def keyword_search(unis_list):
    """
    Функция находит строки которые содержать 'keyword'
    :param unis_list:
    :return:
    """
    found = False
    while not (keyword := input("Введите слово для поиска:")):
        print("Введите допустимое слово!")
    for i in unis_list:
        if keyword in i:
            found = True
            print(i)
    if not found:
        print("Ничего не найдено")


def get_unis_list():
    """
    функция считывает данные из файла и записывает их в список
    :return: unis_list, список с записями из файла
    """
    with open('SibFU.csv', 'r', encoding='utf8') as out_file:
        reader = csv.reader(out_file)
        unis_list = []
        for line in reader:
            unis_list.append(line)
    return unis_list


def get_list_to_add():
    """
    Функция получает и добавляет всю важную информацию о новом университете
    :return: list_do_add, список, с информацией о университете
    """
    list_to_add = []
    uni_name = input("Введите названия университета на английском:")
    year_of_opening = input("Введите год открытия:")
    faculty_no = input("Введите количество факультетов:")
    students_no = input("Введите количество студентов:")
    if uni_name and year_of_opening and faculty_no and students_no:
        list_to_add.extend([uni_name, year_of_opening,
                            faculty_no, students_no])
        return list_to_add
    else:
        print("Данные были введены некорректно!")
        return False


def add_record():
    """
    Функция записывает в файл информацию о Университете,
     которая ранее была собрана в список 'list_to_add'
    :return:
    """
    list_to_add = get_list_to_add()
    if list_to_add:
        with open('SibFU.csv', 'a', encoding='utf8') as out_file:
            writer_object = writer(out_file)
            writer_object.writerow(list_to_add)
            out_file.close()
            print(f"Добавлено {list_to_add}")


def delete_a_record(unis_list):
    """
    функция удаляет строку в файле по значению
    :param unis_list:
    :return:
    """
    found = False
    items_to_delete = []

    while not (keyword := input("Введите слово для поиска:")):
        print("Введите допустимое слово!")

    for i in unis_list:
        if keyword in i:
            found = True
            items_to_delete.append(i)

    if len(items_to_delete) == 1:
        confirm_delete = input(f"delete {items_to_delete}? (Y/N)")
        if confirm_delete.lower() == "y":
            items_to_delete = items_to_delete[0]
    else:
        for item in items_to_delete:
            confirm_delete = input(f"удалить {item}? (Y/N)")
            if confirm_delete.lower() == "y":
                items_to_delete = item
                break

    if not found:
        print("Ничего не найдено")

    if items_to_delete in unis_list:
        unis_list.remove(items_to_delete)

    with open('SibFU.csv', 'w', newline="", encoding='utf8') as out_file:
        writer_to_list = csv.writer(out_file)
        writer_to_list.writerows(unis_list)


def print_menu() -> None:
    """
    menu()
    Выводит графическое меню программы, с возможностью вычисления первого
     n-го обобщённого числа и выхода из нее
    """
    print("""
    1. Загрузить информацию из файла
    2. Поиск по наименованию
    3. Добавить запись
    4. Удалить запись
    5. Выход
    """)


def main() -> None:
    """
    главная функция программы, с возможностью дальнейшего выбора функций для
    реализации заданных задач
    :return:
    """
    unis_list = get_unis_list()
    print_menu()
    choice = input("Что вы хотите сделать: ")
    while choice != "5":
        if choice == "1":
            unis_list = get_unis_list()
            print(*unis_list, sep='\n')
        elif choice == "2":
            keyword_search(unis_list)
        elif choice == "3":
            add_record()
        elif choice == "4":
            delete_a_record(unis_list)
        else:
            print("Введите допустимое значение!")
        print_menu()
        choice = input("Что вы хотите сделать: ")
    print("До свидания!")


if __name__ == "__main__":
    main()
