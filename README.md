## Пример сайта по бронированию отелей на FastAPI.

- Регистрация и авторизация пользователей.
- Добавление, обновление и удаление отелей, комнат и бронирований.

Технологии:

- Аутентификация пользователей (JWT).
- Базы данных. (Postgres, sqlalchemy, alembic-миграции)
- Административная панель. (sqladmin)
- Демонстрационные шаблоны сайта. (Jinja2)
- Очереди задач. (Celery, flower)
- Кэширование. (Redis)
- Тестирование. (Pytest)
- Логирование. (python-json-logger)
- Контейнеризация. (Docker, docker-compose)

## Начало работы.

#### Установить зависимости:

> pip install -r requirements.txt

#### Применить миграции:

> alembic revision --autogenerate -m 'initial' \
> alembic upgrade head

Создать в корне проекта файлы: .env и .env-docker. \
И заполнить по образцу(.env-sample) данными. 

### Локальная разработка:

#### Запустить Celery:

> celery -A app.celery_tasks:app_celery worker --loglevel=INFO -P solo

#### Запустить Flower:

> celery -A app.celery_tasks:app_celery flower

#### Запустить сервер FastApi:

> uvicorn src.main:app --reload


### Тестирование:
> pytest -s -v

### Контейнеризация:

> docker-compose up

