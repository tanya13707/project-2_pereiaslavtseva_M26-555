def parse_value(value: str) -> str | int | bool:
    """Преобразует строку в значение нужного типа."""
    value = value.strip()

    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    
    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False
    try:
        return int(value)
    except ValueError:
        raise ValueError(
            "Значение должно быть целым числом, true/false или строкой в кавычках."
        ) from None


def parse_condition(condition: str) -> dict[str, str | int | bool]:
    """Преобразует условие в словарь."""
    if "=" not in condition:
        raise ValueError("Условие должно содержать знак =.")

    column, value = condition.split("=", 1)
    column = column.strip()

    if not column:
        raise ValueError("Укажите название столбца.")

    return {column: parse_value(value)}