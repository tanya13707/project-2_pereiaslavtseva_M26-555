# Primitive DB

Учебный проект: консольная база данных на Python.

## Запуск

```bash
uv sync
uv run database
```


## управление таблицами

Для столбцов доступны типы: `int`, `str`, `bool`.
Программа автоматически добавляет столбец `ID` с типом `int`.

Команды:

- `create_table <имя_таблицы> <столбец1:тип> ...` — создать таблицу.
- `list_tables` — посмотреть список таблиц.
- `drop_table <имя_таблицы>` — удалить таблицу.
- `help` — открыть справку.
- `exit` — завершить работу программы.

Пример работы с таблицей:

```text
create_table users name:str age:int is_active:bool
list_tables
drop_table users
exit
```

Названия таблиц и их столбцы хранятся в файле `db_meta.json`.