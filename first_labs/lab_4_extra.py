def f1(func):
    def wrapper(*args, **kwargs):
        print("Начало оборачивания функции")
        result = func(*args, **kwargs)
        print(f"Позиционные аргументы - {args}, Ключевые -  {kwargs}")
        print(f"Возвращенное значение: {result} \nОборачивание завершено")
        return result
    return wrapper


@f1
def test(a=123, b="sample"):
    return a, b, "322"


a, b, c = test(12, 33)
