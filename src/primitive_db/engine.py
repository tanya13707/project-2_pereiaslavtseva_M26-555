import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.constants import META_FILE, TYPE_MAP
from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    select,
    update,
)
from primitive_db.parser import parse_condition, parse_value
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


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
    print("\n***Операции с данными***")
    print(
        "<command> insert into <имя_таблицы> "
        "values (<значение1>, <значение2>, ...) - создать запись"
    )
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print(
        "<command> select from <имя_таблицы> "
        "where <столбец> = <значение> - прочитать записи по условию"
    )
    print(
        "<command> update <имя_таблицы> "
        "set <столбец> = <новое_значение> "
        "where <столбец_условия> = <значение_условия> - обновить записи"
    )
    print(
        "<command> delete from <имя_таблицы> "
        "where <столбец> = <значение> - удалить записи"
    )
    print("<command> info <имя_таблицы> - информация о таблице")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def print_table(columns: list[str], table_data: list[dict]) -> None:
    """Выводит записи в виде таблицы."""
    table = PrettyTable()
    table.field_names = columns

    for record in table_data:
        table.add_row([record[column] for column in columns])

    print(table)


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
        elif command == "insert":
            parts = user_input.split(None, 4)

            if (
                len(parts) != 5
                or parts[1] != "into"
                or parts[3] != "values"
            ):
                print("Используйте: insert into <имя_таблицы> values (...)")
                continue

            table_name = parts[2]
            values_text = parts[4].strip()
            if table_name not in metadata:
                print(f'Таблица "{table_name}" не существует.')
                continue

            if not (
                values_text.startswith("(")
                and values_text.endswith(")")
            ):
                print("Значения должны быть в круглых скобках.")
                continue

            values_text = values_text[1:-1].strip()
            try:
                values = [
                    parse_value(value) for value in values_text.split(",")
                ]
                table_data = insert(metadata, table_name, values)
            except ValueError as error:
                print(error)
                continue

            save_table_data(table_name, table_data)
            new_id = table_data[-1]["ID"]
            print(
                f'Запись с ID={new_id} успешно добавлена '
                f'в таблицу "{table_name}".'
            )        
        elif command == "update":
            parts = user_input.split(None, 3)
            if len(parts) != 4 or parts[2] != "set":
                print(
                    "Используйте: update <имя_таблицы> "
                    "set <условие> where <условие>"
                )
                continue

            table_name = parts[1]
            if table_name not in metadata:
                print(f'Таблица "{table_name}" не существует.')
                continue

            set_text, separator, where_text = parts[3].partition(" where ")
            if not separator:
                print("Укажите where и условие отбора записей.")
                continue

            try:
                set_clause = parse_condition(set_text)
                where_clause = parse_condition(where_text)
            except ValueError as error:
                print(error)
                continue
            column_types = {}
            for column in metadata[table_name]:
                column_name, column_type = column.split(":")
                column_types[column_name] = column_type

            if "ID" in set_clause:
                print("ID создаётся автоматически и не изменяется.")
                continue

            if (
                not set_clause.keys() <= column_types.keys()
                or not where_clause.keys() <= column_types.keys()
            ):
                print("Указанный столбец не существует.")
                continue
            valid_types = True
            for clause in (set_clause, where_clause):
                for column_name, value in clause.items():
                    column_type = column_types[column_name]
                    if type(value) is not TYPE_MAP[column_type]:
                        print(
                            f'Столбец "{column_name}" должен '
                            f'иметь тип {column_type}.'
                        )
                        valid_types = False

            if not valid_types:
                continue
            table_data = load_table_data(table_name)
            records = select(table_data, where_clause)
            if not records:
                print("Записи по условию не найдены.")
                continue

            table_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, table_data)

            for record in records:
                print(
                    f'Запись с ID={record["ID"]} '
                    f'в таблице "{table_name}" успешно обновлена.'
                )
        elif command == "delete":
            parts = user_input.split(None, 4)
            if (
                len(parts) != 5
                or parts[1] != "from"
                or parts[3] != "where"
            ):
                print(
                    "Используйте: delete from <имя_таблицы> "
                    "where <условие>"
                )
                continue

            table_name = parts[2]
            if table_name not in metadata:
                print(f'Таблица "{table_name}" не существует.')
                continue

            try:
                where_clause = parse_condition(parts[4])
            except ValueError as error:
                print(error)
                continue
            column_types = {}
            for column in metadata[table_name]:
                column_name, column_type = column.split(":")
                column_types[column_name] = column_type

            valid_condition = True
            for column_name, value in where_clause.items():
                if column_name not in column_types:
                    print("Указанный столбец не существует.")
                    valid_condition = False
                    break

                column_type = column_types[column_name]
                if type(value) is not TYPE_MAP[column_type]:
                    print(
                        f'Столбец "{column_name}" должен '
                        f'иметь тип {column_type}.'
                    )
                    valid_condition = False
                    break

            if not valid_condition:
                continue
            table_data = load_table_data(table_name)
            records = select(table_data, where_clause)
            if not records:
                print("Записи по условию не найдены.")
                continue

            table_data = delete(table_data, where_clause)
            save_table_data(table_name, table_data)

            for record in records:
                print(
                    f'Запись с ID={record["ID"]} успешно удалена '
                    f'из таблицы "{table_name}".'
                )
        elif command == "info":
            if len(args) != 2:
                print("Используйте: info <имя_таблицы>")
                continue

            table_name = args[1]
            if table_name not in metadata:
                print(f'Таблица "{table_name}" не существует.')
                continue

            table_data = load_table_data(table_name)
            print(f"Таблица: {table_name}")
            print(f"Столбцы: {', '.join(metadata[table_name])}")
            print(f"Количество записей: {len(table_data)}")        
        elif command == "select":
            if len(args) < 3 or args[1] != "from":
                print("Используйте: select from <имя_таблицы>")
                continue

            table_name = args[2]

            if table_name not in metadata:
                print(f'Таблица "{table_name}" не существует.')
                continue
            where_clause = None

            if len(args) > 3:
                if args[3] != "where" or len(args) < 5:
                    print("После имени таблицы укажите where <условие>.")
                    continue

                condition = user_input.split(None, 4)[4]

                try:
                    where_clause = parse_condition(condition)
                except ValueError as error:
                    print(error)
                    continue
                column_types = {}
                for column in metadata[table_name]:
                    column_name, column_type = column.split(":")
                    column_types[column_name] = column_type

                valid_condition = True
                for column_name, value in where_clause.items():
                    if column_name not in column_types:
                        print("Указанный столбец не существует.")
                        valid_condition = False
                        break

                    column_type = column_types[column_name]
                    if type(value) is not TYPE_MAP[column_type]:
                        print(
                            f'Столбец "{column_name}" должен '
                            f'иметь тип {column_type}.'
                        )
                        valid_condition = False
                        break

                if not valid_condition:
                    continue

            table_data = load_table_data(table_name)
            records = select(table_data, where_clause)
            columns = [
                column.split(":")[0] for column in metadata[table_name]
            ]
            print_table(columns, records)
        else:
            print(f"Функции {command} нет. Попробуйте снова.")        