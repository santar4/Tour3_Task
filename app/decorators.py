import time  # Імпортуємо модуль time
from functools import wraps


def measure_time(func):
    """Декоратор для вимірювання часу виконання функції."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'Функція {func.__name__} виконалася за {end_time - start_time:.4f} секунд')
        return result

    return wrapper
