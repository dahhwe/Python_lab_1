import math
import random
from typing import Tuple, Union

from sympy import randprime


def _pad_for_encryption(data: bytes, block_size: int) -> bytes:
    """ Добавляет паддинг к данным для шифрования.
    Args:
        data (bytes): Данные для шифрования.
        block_size (int): Размер блока.
    Returns:
        bytes: Данные с паддингом.
    """
    padding_size = block_size - (len(data) % block_size)
    padding = bytes([padding_size]) * padding_size
    return data + padding


def _unpad_after_decryption(data: bytes) -> bytes:
    """ Удаляет паддинг из данных после расшифровки.
    Args:
        data (bytes): Расшифрованные данные с паддингом.
    Returns:
        bytes: Данные без паддинга.
    """
    padding_size = data[-1]
    return data[:-padding_size]


def _calculate_phi(p: int, q: int) -> int:
    """Вычисление функции Эйлера для двух простых чисел.
    Args:
        p (int): Простое число.
        q (int): Простое число.
    Returns:
        int: Значение функции Эйлера для p и q.
    """
    return (p - 1) * (q - 1)


class RSA:
    def __init__(self, number_of_digits: int) -> None:
        """Инициализация класса с указанием количества цифр в простых числах.
        Args:
            number_of_digits (int): Количество цифр в простых числах.
        """
        self.number_of_digits = number_of_digits

    def _generate_prime(self) -> int:
        """Генерация простого числа в заданном диапазоне цифр.
        Returns:
            int: Сгенерированное простое число.
        """
        min_value = 10 ** (self.number_of_digits // 2 - 1)
        max_value = 10 ** (self.number_of_digits // 2) - 1
        return randprime(min_value, max_value)

    def key_gen(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Генерация открытого и закрытого ключей.
        Returns:
            Tuple[Tuple[int, int], Tuple[int, int]]: Кортеж, содержащий открытый и закрытый ключи.
        """
        p = self._generate_prime()
        q = self._generate_prime()
        n = p * q

        phi_n = _calculate_phi(p, q)

        e = random.randint(3, phi_n - 1)
        while math.gcd(e, phi_n) != 1:
            e = random.randint(3, phi_n - 1)

        d = pow(e, -1, phi_n)

        return (e, n), (d, n)

    @staticmethod
    def encrypt(data: Union[bytes, str], public_key: Tuple[int, int], data_type: str) -> list[int | bytes] | bytes:
        """ Шифрование данных с использованием открытого ключа RSA.
        Args:
            data (Union[bytes, str]): Данные для шифрования.
            public_key (Tuple[int, int]): Открытый ключ RSA.
            data_type (str): Тип данных ('file' или 'str').
        Returns:
            bytes: Зашифрованные данные.
        Raises:
            ValueError: Если тип данных не поддерживается.
        """
        key, N = public_key
        encrypted_blocks = []

        if data_type == 'str':
            message_bytes = data.encode('utf-8')
            message_number = int.from_bytes(message_bytes, 'big')
            block_size = N.bit_length() - 1
            mask = (1 << block_size) - 1
            encrypted_blocks = []
            while message_number > 0:
                block = message_number & mask
                message_number >>= block_size
                encrypted_block = pow(block, key, N)
                encrypted_blocks.append(encrypted_block)
            return encrypted_blocks

        if data_type == 'file':
            block_size = N.bit_length() // 8
            data = _pad_for_encryption(data, block_size)

            encrypted_blocks = []
            for i in range(0, len(data), block_size):
                block = int.from_bytes(data[i:i + block_size], byteorder='big')
                encrypted_block = pow(block, key, N)
                encrypted_blocks.append(encrypted_block.to_bytes(block_size + 1, byteorder='big'))

            return b''.join(encrypted_blocks)
        else:
            raise ValueError("Unsupported data type for encryption")

    @staticmethod
    def decrypt(encrypted_data: bytes | list[int], private_key: Tuple[int, int], data_type: str) -> str | bytes:
        """ Расшифровка данных с использованием закрытого ключа RSA.
        Args:
            encrypted_data (bytes): Зашифрованные данные.
            private_key (Tuple[int, int]): Закрытый ключ RSA.
            data_type (str): Тип данных ('file' или 'str').
        Returns:
            bytes: Расшифрованные данные.
        Raises:
            ValueError: Если тип данных не поддерживается.
        """
        key, N = private_key

        if data_type == "str":
            decrypted_blocks = []
            for encrypted_block in encrypted_data:
                decrypted_block = pow(int(encrypted_block), key, N)
                decrypted_blocks.append(decrypted_block)

            block_size = N.bit_length() - 1

            message_number = 0

            for decrypted_block in reversed(decrypted_blocks):
                message_number = (message_number << block_size) | decrypted_block

            message_bytes = message_number.to_bytes(message_number.bit_length() // 8 + 1, 'big').lstrip(b'\x00')

            message_text = message_bytes.decode('utf-8')

            return message_text

        if data_type == 'file':
            block_size = N.bit_length() // 8
            decrypted_data = b''

            for i in range(0, len(encrypted_data), block_size + 1):
                block = int.from_bytes(encrypted_data[i:i + block_size + 1], byteorder='big')
                decrypted_block = pow(block, key, N)
                decrypted_data += decrypted_block.to_bytes(block_size, byteorder='big')

            decrypted_data = _unpad_after_decryption(decrypted_data)
            return decrypted_data
        else:
            raise ValueError("Unsupported data type for decryption")
