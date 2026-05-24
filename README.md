# Org Structure API

REST API для управления организационной структурой — отделами и сотрудниками.

## Технологии

- Python 3.12 / FastAPI
- SQLAlchemy 2.0 async
- PostgreSQL 16
- Alembic
- Docker / docker-compose
- pytest + httpx

## Архитектура

Проект разделён на слои:
- **routers** — HTTP, валидация запросов
- **services** — бизнес-логика, проверки
- **repositories** — работа с БД
- **models** — SQLAlchemy модели
- **schemas** — Pydantic схемы

## Запуск

```bash
git clone https://github.com/kit-kosatka/org-structure-api.git
cd org-structure-api
docker-compose up --build
```

Документация: http://localhost:8000/docs

## Тесты

```bash
# Поднять БД
docker-compose up db -d

# Запустить
pytest
```