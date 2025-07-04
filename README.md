[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)

# Консольное хранилище данных (In-Memory Database)

Простое интерактивное приложение для управления данными в оперативной памяти с поддержкой транзакций.

## Возможности

- **Базовые операции**: 
  - `SET` - сохранение значения
  - `GET` - получение значения
  - `UNSET` - удаление значения
- **Аналитика**:
  - `COUNTS` - подсчёт значений
  - `FIND` - поиск ключей по значению
- **Транзакции**:
  - `BEGIN` - начало транзакции.
  - `ROLLBACK` - откат текущей (самой внутренней) транзакции
  - `COMMIT` - фиксация изменений текущей (самой внутренней) транзакции
  - Поддержка произвольной глубины вложенности

## Установка

1. Склонируйте репозиторий: ```git clone git@github.com:Kesh113/IO_Database.git```
2. Проверьте работоспособность приложения: ```python3 test_database.py```
3. Запустите приложение в консоли: ```python3 io_database.py```

## Структура проекта

├── io_database.py # Основной модуль

├── test_database.py # Юнит-тесты

└── tests.json # Тестовые сценарии

## Примеры запросов

**Базовые операции**:
```
> GET A
NULL
> SET A 10
> GET A
10
> COUNTS 10
1
> SET B 20
> SET C 10
> COUNTS 10
2
> UNSET B
> GET B
NULL
> END
```
**Транзакции**:
```
> BEGIN
> SET A 10
> BEGIN
> SET A 20
> BEGIN
> SET A 30
> GET A
30
> ROLLBACK
> GET A
20
> COMMIT
> GET A
20
```
