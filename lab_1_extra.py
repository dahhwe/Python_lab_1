animals = ['Дракон', 'Змея', 'Лошадь', 'Овца',
           'Обезьяна', 'Петух', 'Собака', 'Свинья',
           'Крыса', 'Бык', 'Тигр', 'Заяц']


def main() -> None:
    while not (dob := input(f"Введите ваш год рождения:")) \
            or not dob.isdigit():
        print(f"Ну так нельзя... Введите ваш год верно!")
    remainder = (int(dob) - 2000) % 12
    sodiac_sign = animals[remainder]

    print(f"Поздравляю, вы {sodiac_sign}!")


if __name__ == "__main__":
    main()
