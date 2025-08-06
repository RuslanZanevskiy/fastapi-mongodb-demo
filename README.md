# Демонстрационный стенд: FastAPI + MongoDB

Этот проект представляет собой готовый `docker-compose` стенд для демонстрации простого CRUD (Create, Read, Update, Delete) API, созданного на FastAPI и использующего MongoDB в качестве базы данных.

## Архитектура

Процесс взаимодействия с сервисом выглядит следующим образом:
```
[Пользователь] <---(HTTP запросы)---> [FastAPI API] <--- (BSON) ---> [MongoDB]
(curl, Postman, etc.)                   (Python)                   (База данных)
```

## Структура проекта

```
.
├── docker-compose.yml      # Главный файл, описывающий все сервисы
├── fastapi-app/
│   ├── Dockerfile          # Dockerfile для сборки образа API
│   ├── main.py             # Код FastAPI приложения (CRUD операции)
│   └── requirements.txt    # Зависимости для Python-скрипта
└── README.md               # Этот файл
```

## Сервисы

* **`mongodb`**: Не реляционная база данных NoSQL, используемая для хранения документов в формате, подобном JSON.
* **`fastapi-app`**: Python-приложение на базе FastAPI, которое предоставляет RESTful API для управления записями пользователей в базе данных.

## Ключевые особенности

* **Простота развертывания**: Все окружение поднимается одной командой `docker compose up`.
* **Стандартный CRUD**: Реализованы все базовые операции: создание, чтение, обновление и удаление пользователей.
* **Автоматическая документация**: FastAPI автоматически генерирует интерактивную документацию API, доступную по адресу `http://localhost:8000/docs`.
* **Сохранность данных**: Данные MongoDB сохраняются между перезапусками в `docker volume`.

## Необходимые условия

* **Docker**
* **Docker Compose v2**

## Запуск проекта

1.  Склонируйте репозиторий 
    ```bash
    git clone https://github.com/RuslanZanevskiy/fastapi-mongodb-demo.git
    ```
2.  Откройте терминал в корневой директории проекта и запустите все сервисы:
    ```bash
    docker compose up -d --build
    ```
    Ключ `--build` обеспечит сборку образа для FastAPI приложения при первом запуске.

## Остановка проекта

* Для остановки всех сервисов и удаления контейнеров:
    ```bash
    docker compose down
    ```
* Для **полной очистки** (включая данные MongoDB):
    ```bash
    docker compose down -v
    ```

## Как использовать API

API будет доступно по адресу `http://localhost:8000`.

### 1. Интерактивная документация (Swagger UI)

Самый простой способ протестировать API — открыть в браузере:
[**http://localhost:8000/docs**](http://localhost:8000/docs)

### 2. Примеры запросов с помощью `curl`

* **Создать нового пользователя:**
    ```bash
    curl -X 'POST' \
      'http://localhost:8000/users/' \
      -H 'Content-Type: application/json' \
      -d '{
        "name": "Ivan Ivanov",
        "email": "ivan.ivanov@example.com"
      }'
    ```

* **Получить список всех пользователей:**
    ```bash
    curl -X 'GET' 'http://localhost:8000/users/'
    ```

* **Получить пользователя по ID** (замените `USER_ID` на реальный ID из ответа на создание или получение списка):
    ```bash
    curl -X 'GET' 'http://localhost:8000/users/USER_ID'
    ```

* **Обновить данные пользователя** (замените `USER_ID`):
    ```bash
    curl -X 'PUT' \
      'http://localhost:8000/users/USER_ID' \
      -H 'Content-Type: application/json' \
      -d '{
        "name": "Petr Petrov"
      }'
    ```

* **Удалить пользователя** (замените `USER_ID`):
    ```bash
    curl -X 'DELETE' 'http://localhost:8000/users/USER_ID'
    ```

### Доступ к MongoDB

1.  Подключиться к командной строке `mongosh` с аутентификацией:
    ```bash
    docker compose exec mongodb mongosh -u root -p example
    ```
2.  Внутри `mongosh` можно выполнять команды:
    ```javascript
    // Показать все базы данных
    show dbs;

    // Переключиться на нашу базу
    use fastapidb;

    // Показать все записи в коллекции 'users'
    db.users.find();
    ```
