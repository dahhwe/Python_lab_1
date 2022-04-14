"""
Дан словарь, ключи которого представляют собой английские слова, а
значения множества слов на русском языке. Программа преобразует
данный англо-русский словарь в русско-английский. Слова в
результирующем словаре находятся в лексикографическом
порядке.
"""
import string


def sort_dict(sorted_dict: dict) -> dict:
    """
    Сортировка словаря
    по ключам в алфавитном порядке
    :param sorted_dict: Отсортированный словарь
    :return:
    """
    sorted_dict = dict(sorted(sorted_dict.items(),
                              key=lambda item: item[0]))
    return sorted_dict


def trans_dict(en_dict: dict[str, list[str]]) -> dict:
    """
    Преобразованный словарь, где ключ меняется мест1
    ом с множеством,
    в случае если у ключа несколько множеств,
    будут созданны дополнтельные ключи для каждго множества
    :param en_dict: англо-русский словарь
    :return: translated_dict русско-английский словарь, где у одного ключа
    может быть несколько значений (несколько переводов у слова).
    """
    translated_dict = {}
    for key, value in en_dict.items():
        for list_values in value:
            if list_values in translated_dict:
                translated_dict[list_values] += [key]
            else:
                translated_dict[list_values] = [key]
    return translated_dict


def output_dict(dict_to_print):
    """
    Красивый вывод словаря
    :param dict_to_print: словарь
    :return:
    """
    for key, value in dict_to_print.items():
        print(f"{key}: {value}")
    print()


def transform_dict(en_dict: dict):
    """
    выводит оригинальный
    и преобразованный словари
    :param en_dict: англо-русский словарь
    :return:
    """
    transformed_dict = trans_dict(en_dict)
    print("Оригинальный словарь")
    output_dict(en_dict)
    print("Преобразованный словарь")
    output_dict(transformed_dict)


def check_valid_input(phrase: str) -> str:
    """
    Функция проверяет полученную переменную
    на правильность и выполняется пока для
    переменной не будет введено действительное значение
    :param phrase: фраза,
    :return:
    """
    while not ((word := input(phrase)) and (word.isalpha())):
        print("Введите допустимое слово!")
    return word


def find_word(en_dict: dict[str, list[str]]) -> None:
    """
    Поиск русского или английского слова в словаре,
    при нахождении выводит перевод этого слова.
    :param en_dict: англо-русский словарь
    :return:
    """
    word_to_find = check_valid_input("Введите слово для поиска:")
    translated_dict = trans_dict(en_dict)

    if word_to_find in en_dict:
        print(f"перевод слова: {en_dict[word_to_find]}")
    elif word_to_find in translated_dict:
        print(f"перевод слова: {str(translated_dict[word_to_find])}")
    else:
        print("Данного слова нет в словаре")


def add_pair(en_dict: dict[str, list[str]]) -> None:
    """
    Функция добавляет слово и перед этого слова (ключ и значение) в словарь
    :param en_dict: англо-русский словарь
    :return: при вводе неверных переменных, возвращается в функцию main()
    """
    phrase_rus = "Введите слово на русском языке, которое хотите добавить:"
    rus_word_to_add = check_valid_input(phrase_rus)
    for letter in rus_word_to_add:
        if letter in string.ascii_letters:
            print("Слово должно быть на русском!")
            return

    phrase_eng = "Введите перевод слова на английском языке:"
    eng_word_to_add = check_valid_input(phrase_eng)
    for letter in eng_word_to_add:
        if letter not in string.ascii_letters:
            print("Слово должно быть на английском!")
            return

    confirm_add = input(f"Добавить {rus_word_to_add}"
                        f" - {eng_word_to_add}? (Y/N)")
    if confirm_add in "Yy":
        added = False
        if eng_word_to_add not in en_dict:
            en_dict.update({eng_word_to_add: [rus_word_to_add]})
            added = True
        else:
            for key, value in en_dict.items():
                if eng_word_to_add == key and \
                        rus_word_to_add not in en_dict[key]:
                    en_dict[key] += [rus_word_to_add]
                    added = True
        if added:
            print("Добавлено!")
            dict_to_output = sort_dict(en_dict)
            output_dict(dict_to_output)
        else:
            print("Не добавлено, такой перевод уже есть")
    else:
        return


def delete_pair_by_key(en_dict: dict[str, list[str]]) -> None:
    """
    Удаляет пару ключ-значение по ключу
    :param en_dict: англо-русский словарь
    :return:
    """
    output_dict(en_dict)
    word_to_delete = check_valid_input("Введите слово,"
                                       " которое хотите удалить:")
    if word_to_delete in en_dict:
        del en_dict[word_to_delete]
        print(f"{word_to_delete} удалено")
    else:
        print("Такого ключа нет")


def print_menu() -> None:
    """
    menu()
    Выводит графическое меню программы, с возможностью вычисления первого
     n-го обобщённого числа и выхода из нее
    """
    print("""
1. Преобразовать словарь
2. Найти слово для перевода
3. Добавить слово
4. Удалить по ключу (English)
5. выход
    """)


def main() -> None:
    """
    главная функция, содержит англо-русский словарь и
    выбор действий
    :return:
    """
    en_to_rus_dict = {'path': ['путь', 'тропа'],
                      'raccoon': ['енот'],
                      'rhino': ['носорог'],
                      'apple': ['яблоко'],
                      'apricot': ['абрикос'],
                      'zucchini': ['кабачок'],
                      'snake': ['змея'],
                      'cat': ['кошка']}

    print_menu()
    choice = input("Что вы хотите сделать: ")
    while choice != "5":
        if choice == "1":
            transform_dict(sort_dict(en_to_rus_dict))
        elif choice == "2":
            find_word(sort_dict(en_to_rus_dict))
        elif choice == "3":
            add_pair(en_to_rus_dict)
        elif choice == "4":
            delete_pair_by_key(en_to_rus_dict)
            output_dict(sort_dict(en_to_rus_dict))
        else:
            print("Введите допустимое значение!")
        print_menu()
        choice = input("Что вы хотите сделать: ")
    print("До свидания!")


if __name__ == "__main__":
    main()
