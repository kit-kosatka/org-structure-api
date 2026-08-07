# Org Structure API

REST API для управления организационной структурой компании — отделами и сотрудниками.

Отделы образуют иерархическое дерево: каждый отдел может иметь родительский и дочерние отделы. Реализована защита от циклических зависимостей и два режима удаления отделов.

## Технологии

- Python 3.12 / FastAPI
- SQLAlchemy 2.0 async
- PostgreSQL 16
- Alembic
- Docker / docker-compose
- pytest + httpx

## Архитектура

Проект разделён на три слоя по принципу Repository Pattern:

- **routers** — HTTP, валидация запросов
- **services** — бизнес-логика, проверки
- **repositories** — работа с БД
- **models** — SQLAlchemy модели
- **schemas** — Pydantic схемы

## Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/v1/departments/` | Создать отдел |
| GET | `/api/v1/departments/{id}` | Получить отдел с деревом дочерних |
| PATCH | `/api/v1/departments/{id}` | Переименовать или переместить отдел |
| DELETE | `/api/v1/departments/{id}` | Удалить отдел |
| POST | `/api/v1/departments/{id}/employees/` | Добавить сотрудника в отдел |

### Параметры GET /departments/{id}

- `depth` (int, default=1, max=5) — глубина дерева дочерних отделов
- `include_employees` (bool, default=true) — включать сотрудников в ответ
- `sort_by` (str, default=created_at) — сортировка сотрудников: `created_at` или `full_name`

### Параметры DELETE /departments/{id}

- `mode=cascade` — удалить отдел, всех сотрудников и дочерние отделы
- `mode=reassign` — перевести сотрудников в другой отдел, затем удалить
- `reassign_to_id` — обязателен при `mode=reassign`

## Бизнес-логика

- Уникальность имени отдела в рамках одного родителя
- Валидация полей: обрезка пробелов, длина 1-200 символов
- Защита от самоссылки и циклических зависимостей в дереве (409 Conflict)
- Каскадное удаление на уровне БД через ondelete=CASCADE

## Запуск

git clone https://github.com/kit-kosatka/org-structure-api.git
cd org-structure-api
docker-compose up --build

Миграции применяются автоматически при запуске.

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

## Тесты

Поднять БД:
docker-compose up db -d

Запустить тесты:
pytest