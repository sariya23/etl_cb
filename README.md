# ETL процесс курс валют

## About

Скрипт выгружает курсы валют в СУБД PostgreSQL. В самой базе также есть "витрины" для работы с данными. Они представлены в виде вибшек

## Локальный запуск

Нужно поднять (в докере или где угодно) базу и в файл `.env` занести информацию для подключения.

```shell
POSTGRES_USERNAME=name  # имя пользователя БД
POSTGRES_PASSWORD=password  # пароль пользователя
POSTGRES_HOST=host  # хост, где крутится БД, например localhost
POSTGRES_PORT=port  # порт, где крутится БД
POSTGRES_DB=db_name  # название БД
```

После этого нужно накатить миграции, чтобы создались нужные таблицы. В корне выполнить
```shell
goose -dir migrations postgres "postgresql://POSTGRES_USERNAME:POSTGRES_PASSWORD@POSTGRES_HOST:POSTGRES_PORT/POSTGRES_DB?sslmode=disable" up
```

Далее нужно поставить зависимости: `requirements.txt` или `pyproject.toml`. 

Запуск скрипта:
```shell
python3 etl.py
```