from primitive_db.constants import VALID_TYPES


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


def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata