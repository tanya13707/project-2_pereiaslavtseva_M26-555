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

## CRUD-операции

CRUD - это добавление, просмотр, изменение и удаление записей.

Данные каждой таблицы хранятся в отдельном JSON-файле в папке `data/`.
Например, данные таблицы `users` хранятся в `data/users.json`.

Команды:

- `insert into <имя_таблицы> values (<значение1>, <значение2>, ...)` - добавить запись.
- `select from <имя_таблицы>` - показать все записи.
- `select from <имя_таблицы> where <столбец> = <значение>` — найти записи по условию.
- `update <имя_таблицы> set <столбец> = <новое_значение> where <столбец_условия> = <значение_условия>` - изменить записи по условию.
- `delete from <имя_таблицы> where <столбец> = <значение>` — удалить записи по условию.
- `info <имя_таблицы>` - показать столбцы и количество записей.

Все поля обязательны. Значения нужно передавать в порядке столбцов таблицы.
Значение `ID` вводить не нужно: программа создаёт его автоматически.

Строки пишутся в кавычках, целые числа - без кавычек.
Для логических значений используются `true` и `false`.

Пример работы с записями:

```text
create_table users name:str age:int is_active:bool
insert into users values ("Sergei", 28, true)
select from users
select from users where age = 28
update users set age = 29 where name = "Sergei"
select from users
delete from users where ID = 1
info users
exit
```

## Демонстрация

[![asciicast](https://asciinema.org/a/a2SJSuDrjqoZEqkZ.svg)](https://asciinema.org/a/a2SJSuDrjqoZEqkZ)

### CRUD-операции

[![asciicast](https://asciinema.org/a/7zzDXfiPTtReB8Jw.svg)](https://asciinema.org/a/7zzDXfiPTtReB8Jw)