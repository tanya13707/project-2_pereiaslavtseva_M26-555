from primitive_db.constants import TYPE_MAP, VALID_TYPES
from primitive_db.decorators import confirm_action, handle_db_errors, log_time
from primitive_db.utils import load_table_data


def create_table(metadata, table_name, columns):
    """Создаёт новую таблицу и проверяет её столбцы."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata
    
    for column in columns:
        parts = column.split(":")

        if len(parts) != 2:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        column_name, column_type = parts

        if not column_name or column_type not in VALID_TYPES:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata
        if column_name == "ID" and column_type != "int":
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata
    table_columns = ["ID:int"]
    for column in columns:
        if column != "ID:int":
            table_columns.append(column)

    metadata[table_name] = table_columns
    columns_text = ", ".join(table_columns)
    print(
        f'Таблица "{table_name}" успешно создана '
        f"со столбцами: {columns_text}"
    )
    return metadata


@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Добавляет новую запись в таблицу."""
    if table_name not in metadata:
        raise KeyError(table_name)

    columns = metadata[table_name][1:]

    if len(values) != len(columns):
        raise ValueError(
            "Количество значений должно совпадать с количеством столбцов без ID."
        )

    for column, value in zip(columns, values):
        column_name, column_type = column.split(":")
        expected_type = TYPE_MAP[column_type]

        if type(value) is not expected_type:
            raise ValueError(
                f'Столбец "{column_name}" должен иметь тип {column_type}.'
            )

    table_data = load_table_data(table_name)

    new_id = 1
    for record in table_data:
        if record["ID"] >= new_id:
            new_id = record["ID"] + 1

    new_record = {"ID": new_id}

    for column, value in zip(columns, values):
        column_name = column.split(":")[0]
        new_record[column_name] = value

    table_data.append(new_record)
    return table_data            


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает все записи или записи по условию."""
    if where_clause is None:
        return table_data

    selected_records = []

    for record in table_data:
        matches = True

        for column_name, value in where_clause.items():
            if record[column_name] != value:
                matches = False
                break

        if matches:
            selected_records.append(record)

    return selected_records


@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Обновляет записи по условию."""
    selected_records = select(table_data, where_clause)
    if selected_records is None:
        return None

    for record in selected_records:
        record.update(set_clause)

    return table_data


@handle_db_errors
@confirm_action("удаление записей")
def delete(table_data, where_clause):
    """Удаляет записи по условию."""
    selected_records = select(table_data, where_clause)
    if selected_records is None:
        return None
    
    remaining_records = []

    for record in table_data:
        if record not in selected_records:
            remaining_records.append(record)

    return remaining_records