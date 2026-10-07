import shlex

import prompt

from primitive_db.constants import META_FILE
from primitive_db.core import create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata


def welcome():
    print("Первая попытка запустить проект!")
    print()
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        command = prompt.string("Введите команду: ")

        if command == "exit":
            break
        elif command == "help":
            print()
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")


def print_help():
    """Prints the help message for the current mode."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print(
        "<command> create_table <имя_таблицы> <столбец1:тип> .. "
        "- создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    """Запускает основной цикл базы данных."""
    print_help()

    while True:
        metadata = load_metadata(META_FILE)
        user_input = prompt.string("Введите команду: ")

        try:
            args = shlex.split(user_input)
        except ValueError:
            print(f"Некорректное значение: {user_input}. Попробуйте снова.")
            continue

        if not args:
            continue

        command = args[0]

        if command == "exit":
            break
        elif command == "help":
            print_help()
        elif command == "list_tables":
            for table_name in metadata:
                print(f"- {table_name}")
        elif command == "create_table":
            if len(args) < 3:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue

            table_name = args[1]
            columns = args[2:]
            table_count = len(metadata)

            metadata = create_table(metadata, table_name, columns)

            if len(metadata) > table_count:
                save_metadata(META_FILE, metadata)
        elif command == "drop_table":
            if len(args) != 2:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue

            table_name = args[1]
            table_count = len(metadata)

            metadata = drop_table(metadata, table_name)

            if len(metadata) < table_count:
                save_metadata(META_FILE, metadata)
        else:
            print(f"Функции {command} нет. Попробуйте снова.")        