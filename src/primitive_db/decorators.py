import time


def handle_db_errors(func):
    """Обрабатывает ошибки при работе с базой данных."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: файл данных не найден.")
        except KeyError as error:
            print(f"Ошибка: таблица или столбец {error} не найден.")
        except ValueError as error:
            print(f"Ошибка валидации: {error}")

    return wrapper


def confirm_action(action_name):
    """Запрашивает подтверждение перед выполнением операции."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )
            if answer != "y":
                print("Операция отменена.")
                return None
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    """Выводит время выполнения функции."""
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        elapsed_time = time.monotonic() - start_time
        print(
            f"Функция {func.__name__} выполнилась за "
            f"{elapsed_time:.3f} секунд"
        )
        return result

    return wrapper


def create_cacher():
    """Создаёт функцию для кэширования результатов."""
    cache = {}

    def cache_result(key, value_func):
        """Возвращает сохранённый результат или вычисляет новый."""
        if key not in cache:
            cache[key] = value_func()
        return cache[key]

    return cache_result