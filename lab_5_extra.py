"""
Проверка пароля на надежность
"""
import re


def check(pass_to_check):
    return False if not re.search('[A-Z]', pass_to_check) or \
                    not re.search('[a-z]', pass_to_check) or \
                    not re.search('[0-9]', pass_to_check) or \
                    not re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]',
                                  pass_to_check) else True


if __name__ == '__main__':
    while not (password := input("Введите пароль для проверки:")):
        print("Пароль не может быть пустым!")
    print("Сложный пароль") if check(password) else print("Слабый пароль")
