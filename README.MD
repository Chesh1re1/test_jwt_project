# Django JWT API Project

Проект на Django REST Framework с JWT аутентификацией, PostgreSQL, Redis, Celery и Docker.

## Технологии

- **Django 5.2** - веб-фреймворк
- **Django REST Framework** - создание API
- **JWT (Simple JWT)** - аутентификация
- **PostgreSQL 15** - база данных
- **Redis** - кеширование и брокер сообщений
- **Celery** - асинхронные задачи
- **Celery Beat** - периодические задачи
- **Flower** - мониторинг Celery
- **Docker** - контейнеризация

## Функционал

- ✅ JWT аутентификация (access/refresh токены)
- ✅ Кеширование запросов с Redis
- ✅ Периодические задачи через Celery Beat (отчеты каждые 2 минуты)
- ✅ Docker контейнеризация всех сервисов

## Структура проекта
```text
test_jwt_project/
├── jwt_app/ # Основное приложение
│ ├── models.py # Модели данных
│ ├── views.py # API эндпоинты
│ ├── serializers.py # Сериализаторы
│ ├── tasks.py # Celery задачи
│ └── tests.py # Тесты
├── test_app/ # Конфигурация проекта
│ ├── settings.py
│ ├── celery.py
│ └── urls.py
├── reports/ # Директория для отчетов Celery (создается автоматически)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```
## Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Git
- Python 3.11+ (для локальной разработки)

### 1. Клонирование репозитория

```bash
git clone https://github.com/Chesh1re1/test_jwt_project
cd test_jwt_project/test_app
```
### 2. Настройка переменных окружения
Создайте файл .env в директории test_app проекта:
```.env
# PostgreSQL
PG_DB=jwt_db
PG_USER=jwt_user
PG_PWD=jwt_password
PG_HOST=db
PG_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Суперпользователь (создается автоматически)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123
```
# 3. Запуск через Docker

```bash
# Сборка и запуск контейнеров
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Остановка контейнеров
docker-compose down
```
После запуска будут доступны:

Django приложение: http://localhost:8000

Flower (мониторинг Celery): http://localhost:5555