import os


def read_file_in_binary_mode(file_path: str) -> bytes:
    """
    Читает содержимое файла в бинарном режиме.

    :param file_path: Путь к файлу для чтения.
    :return: Содержимое файла в виде байтового массива.
    """
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except IOError as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return b''


def write_data_to_file(file_path: str, data: bytes | str, mode: str = 'wb') -> None:
    """
    Записывает данные в файл.

    :param file_path: Путь к файлу для записи.
    :param data: Данные для записи.
    :param mode: Режим записи ('w' для текстовых файлов, 'wb' для бинарных).
    """
    try:
        with open(file_path, mode) as file:
            file.write(data)
    except IOError as e:
        print(f"Ошибка при записи в файл {file_path}: {e}")


def encrypt_and_write_to_file(file_path: str, encrypted_data: str) -> None:
    """
    Шифрует и записывает данные в файл с добавлением суффикса '_encrypted'.

    :param file_path: Путь к исходному файлу.
    :param encrypted_data: Зашифрованные данные для записи.
    """
    base, _ = os.path.splitext(file_path)
    encrypted_file_path = f"{base}_encrypted.txt"
    write_data_to_file(encrypted_file_path, encrypted_data)


def read_encrypted_data_from_file(file_path: str) -> str:
    """
    Читает зашифрованные данные из файла с расширением .txt.

    :param file_path: Путь к файлу с зашифрованными данными.
    :return: Зашифрованные данные в виде строки или None в случае ошибки.
    """
    _, ext = os.path.splitext(file_path)
    if ext != ".txt":
        print(f"Файл {file_path} не имеет расширения .txt и не может быть прочитан как зашифрованный файл.")
        return ""
    return read_file_in_binary_mode(file_path).decode('utf-8')


def decrypt_and_write_to_file(encrypted_file_path: str, decrypted_data: str, extension: str) -> None:
    """
    Расшифровывает данные и записывает их в файл, удаляя суффикс '_encrypted'.

    :param encrypted_file_path: Путь к зашифрованному файлу.
    :param decrypted_data: Расшифрованные данные для записи.
    :param extension: Расширение файла после расшифровки.
    """
    base = os.path.splitext(encrypted_file_path)[0]
    if not base.endswith('_encrypted'):
        print(f"Файл {encrypted_file_path} не оканчивается на '_encrypted', возможно он не зашифрован.")
        return
    decrypted_file_path = f"{base[:-10]}_decrypted{extension}"
    write_data_to_file(decrypted_file_path, decrypted_data, 'wb')
