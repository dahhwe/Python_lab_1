import string
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from colorama import init, Fore


def highlight_substrings(string: str, substrings: list[str]) -> str:
    init()
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
              Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    for i, substring in enumerate(substrings):
        color = colors[i % len(colors)]
        string = string.replace(substring, f"{color}{substring}{Fore.RESET}")
    return string


def replacement(substring: str):
    letters = string.ascii_letters + ''.join([chr(i) for i in range(ord('А'), ord('А') + 32)]) + ''.join(
        [chr(i) for i in range(ord('а'), ord('а') + 32)])
    words = []
    for i in range(len(substring)):
        for j in letters:
            substring_copy = substring.replace(substring[i], j, 1)
            words.append(substring_copy)
    return words


def delete_sub(substring: str):
    words = []
    for i in range(len(substring)):
        substring_copy = substring.replace(substring[i], '', 1)
        words.append(substring_copy)
    return words


def insert_sub(substring: str):
    letters = string.ascii_letters + ''.join([chr(i) for i in range(ord('А'), ord('А') + 32)]) + ''.join(
        [chr(i) for i in range(ord('а'), ord('а') + 32)])

    def insert(source_str, insert_str, pos):
        return source_str[:pos] + insert_str + source_str[pos:]

    words = []
    for i in range(len(substring) + 1):
        for j in letters:
            words.append(insert(substring, j, i))
    return words


def permutation(substring: str):
    words = []
    for i in range(len(substring) - 1):
        for j in range(i, len(substring)):
            s_copy = list(substring)
            s_copy[i], s_copy[j] = s_copy[j], s_copy[i]
            words.append(''.join(s_copy))
    return words


def search_first(string: str, sub_string: str,
                 case_sensitivity: bool) -> tuple[int | Any, ...] | None:
    results = []
    if not case_sensitivity:
        string = string.lower()
        sub_string = sub_string.lower()
    size_text = len(string)
    size_substring = len(sub_string)
    if size_text < size_substring:
        return None
    data = {}
    for i in range(size_substring):
        if sub_string[size_substring - i - 1] not in data:
            if i == 0:
                data[sub_string[size_substring - 1]] = size_substring
            else:
                data[sub_string[size_substring - i - 1]] = i
        elif sub_string[size_substring - i - 1] == sub_string[size_substring - 1] and i != 0:
            data[sub_string[size_substring - 1]] = min(data[sub_string[size_substring - 1]], i)
    i = 0
    j = size_substring - 1
    while j >= 0 and i <= size_text - size_substring:
        if j == 0 and string[i + j] == sub_string[j]:
            results.append(i)
            i = i + 1
            j = size_substring - 1
            continue
        elif string[i + j] == sub_string[j]:
            j = j - 1
            continue
        else:
            if string[i + j] in sub_string:
                i = i + data.get(string[i + j])
            else:
                i = i + data.get(sub_string[size_substring - 1])
            j = size_substring - 1
            continue
    if len(results) != 0:
        return tuple(results)
    else:
        return None


def search_wrong(string: str, substring: str,
                 case_sensitivity: bool, errors: int):
    if not case_sensitivity:
        string = string.lower()
        substring = substring.lower()
    n = len(string)
    m = len(substring)
    beam_width = errors + 1
    result_indices = []

    for start in range(n - m + 1):
        state = (0, 0)
        queue = [state]
        while queue:
            current_errors, index = queue.pop(0)
            if current_errors > errors:
                continue
            if index == m:
                result_indices.append(start)
                break
            next_char = substring[index]
            if string[start + index] == next_char:
                queue.append((current_errors, index + 1))
            else:
                queue.append((current_errors + 1, index + 1))
                queue.append((current_errors + 1, index))
                queue.append((current_errors + 1, index + 2))
            queue.sort(key=lambda x: x[0])
            queue = queue[:beam_width]
    return tuple(result_indices)


def func(string: str, substring: str,
         case_sensitivity: bool, errors: int, threads: int):
    wrong_words = []
    wrong_words.extend(replacement(substring))
    wrong_words.extend(delete_sub(substring))
    wrong_words.extend(insert_sub(substring))
    wrong_words.extend(permutation(substring))

    result = set()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(lambda x: search_first(string, x, case_sensitivity), wrong_words)

    for r in results:
        if r:
            r = set(r)
            result = result.union(r)

    # Фильтрация результатов с учетом количества допустимых ошибок
    filtered_result = set()
    for index in result:
        found_substring = string[index:index + len(substring)]
        distance = levenshtein_distance(found_substring, substring)
        if distance <= errors:
            filtered_result.add(index)

    return tuple(filtered_result)


def processing_results(result: dict[str, tuple[int]], method: str) -> dict[str, tuple[int]]:
    if isinstance(result, tuple):
        if method == 'first':
            result = tuple(sorted(result))
        else:
            result = tuple(reversed(sorted(result)))
    else:
        list_results = []
        for i in result:
            if result[i] is not None:
                for j in result[i]:
                    list_results.append(j)
        for i in result:
            if result[i] is not None:
                if method == 'first':
                    result[i] = tuple(sorted(result[i]))
                else:
                    result[i] = tuple(reversed(sorted(result[i])))
    return result


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Вычисление расстояния Левенштейна между двумя строками
    """
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]
