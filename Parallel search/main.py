import os
from argparse import ArgumentParser

from search import search_wrong, search_first, highlight_substrings


def main():
    """
    Основная функция для запуска утилиты поиска подстроки в строке.
    """
    parser = ArgumentParser(description="Утилита для нечеткого поиска подстроки в строке.")
    parser.add_argument("-s", "--string", type=str,
                        help="Строка для поиска. Если не указана, то используется содержимое файла, указанного с "
                             "помощью аргумента --file.")
    parser.add_argument("-f", "--file", type=str,
                        help="Путь к файлу для поиска. Если указан, то содержимое файла используется вместо строки "
                             "для поиска.")
    parser.add_argument("-ss", "--sub-string", type=str,
                        nargs="+", required=True,
                        help="Подстрока или подстроки для поиска.")
    parser.add_argument("-cs", "--case-sensitivity",
                        action="store_true", default=False,
                        help="Если указано, то поиск будет чувствителен к регистру.")
    parser.add_argument("-m", "--method",
                        choices=("first", "last"), default="first",
                        help="Метод сортировки результатов. Если указано 'first', то результаты будут отсортированы в "
                             "порядке возрастания индексов вхождений. Если указано 'last', то результаты будут "
                             "отсортированы в порядке убывания индексов вхождений.")
    parser.add_argument("-c", "--count", type=int, default=None,
                        help="Количество первых вхождений каждой подстроки для поиска. Если не указано, то будут "
                             "найдены все вхождения.")
    parser.add_argument("-ml", "--max-lines", type=int, default=10,
                        help="Максимальное количество строк для вывода результата.")
    parser.add_argument("-e", "--errors", type=int, default=0,
                        help="Количество допустимых ошибок в словах подстроки при парсинге.")
    parser.add_argument("-t", "--threads", type=int, default=1,
                        help="Количество потоков для параллельного поиска.")
    parser.add_argument("-o", "--output-file", type=str,
                        help="Базовое имя файла для вывода результата. Если указано, то результат будет записан в файл с указанным именем и наибольшим доступным номером вместо вывода в консоль.")

    args = parser.parse_args()

    if args.string:
        string = args.string
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            string = f.read()
    else:
        raise ValueError("Either --string or --file argument must be provided")

    sub_strings = args.sub_string
    case_sensitivity = args.case_sensitivity
    method = args.method
    count = args.count
    max_lines = args.max_lines
    errors = args.errors
    threads = args.threads

    result_indices = set()

    output_lines = []

    for sub_string in sub_strings:
        # Выполнение нечеткого поиска с использованием алгоритма расширения выборки
        fuzzy_indices = search_wrong(string, sub_string, case_sensitivity, errors)
        result_indices.update(fuzzy_indices)

        # Выполнение точного поиска подстроки в строке
        exact_indices = search_first(string, sub_string, case_sensitivity)
        if exact_indices is None:
            output_lines.append(f"No matches found for substring: {sub_string}\n")
            continue
        else:
            result_indices.update(exact_indices)

        # Генерация списка ошибочных и точных подстрок для выделения в исходной строке
        substrings_to_highlight = []

        for index in result_indices:
            substrings_to_highlight.append(string[index:index + len(sub_strings[0])])

        # Цветовое выделение найденных подстрок
        highlighted_string = highlight_substrings(string, substrings_to_highlight)
        print(highlighted_string)

        # Ограничение на количество выводимого текста (не более 10 строк)
        result_lines = str(result_indices).split('\n')
        if len(result_lines) > max_lines:
            result_indices_str = '\n'.join(result_lines[:max_lines]) + '...'

        # Цветовое выделение найденных подстрок
        highlighted_string = highlight_substrings(string, substrings_to_highlight)

        output_lines.append(f"Substring: {sub_string}")
        output_lines.append("Exact matches:")
        for index in exact_indices:
            output_lines.append(f"  - {string[index:index + len(sub_string)]} at index {index}")
        output_lines.append("Fuzzy matches:")
        for index in fuzzy_indices:
            start_index = string.rfind(' ', 0, index) + 1
            end_index = string.find(' ', index)
            if end_index == -1:
                end_index = len(string)
            output_lines.append(f"  - {string[start_index:end_index]} at index {index}")
        output_lines.append("")

    if args.output_file:
        file_number = 1
        while os.path.exists(f"{args.output_file}{file_number}.txt"):
            file_number += 1
        with open(f"{args.output_file}{file_number}.txt", 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
    print('\n'.join(output_lines))


if __name__ == '__main__':
    main()
