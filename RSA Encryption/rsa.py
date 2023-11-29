import math
import random

from sympy import randprime


def _pad_for_encryption(data, block_size):
    padding_size = block_size - (len(data) % block_size)
    padding = bytes([padding_size]) * padding_size
    return data + padding


# Helper function to remove padding after decryption
def _unpad_after_decryption(data):
    padding_size = data[-1]
    return data[:-padding_size]


def _calculate_phi(p, q):
    """Вычисление функции Эйлера для двух простых чисел."""
    return (p - 1) * (q - 1)


class RSA:
    def __init__(self, number_of_digits):
        """Инициализация класса с указанием количества цифр в простых числах."""
        self.number_of_digits = number_of_digits

    def _generate_prime(self):
        """Генерация простого числа в заданном диапазоне цифр."""
        min_value = 10 ** (self.number_of_digits // 2 - 1)
        max_value = 10 ** (self.number_of_digits // 2) - 1
        return randprime(min_value, max_value)

    def key_gen(self):
        """Генерация открытого и закрытого ключей."""
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
    def encrypt(data, public_key, data_type):
        key, N = public_key
        encrypted_blocks = []

        if data_type == 'file':
            # Ensure the data is padded to a multiple of the block size
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
    def decrypt(encrypted_data, private_key, data_type):
        key, N = private_key
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
