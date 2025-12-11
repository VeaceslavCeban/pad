
# Microservices Shop (фиксированная версия с CORS)

Это доработанная микросервисная версия магазина:

- отдельные сервисы на FastAPI:
  - `users_service` — пользователи
  - `products_service` — товары
  - `orders_service` — заказы
  - `inventory_service` — склад
  - `payments_service` — платежи
  - `notifications_service` — уведомления
- `frontend` — простой фронтенд (FastAPI + HTML + JS), который ходит по REST к сервисам
- **CORS настроен во всех микросервисах**, чтобы фронтенд мог к ним обращаться с `http://localhost:8000`
- docker-compose для поднятия всей системы
- unit-тесты для каждого сервиса (pytest)

## 1. Структура

```text
microservices_shop_fixed/
  docker-compose.yml
  README.md

  users_service/
  products_service/
  orders_service/
  inventory_service/
  payments_service/
  notifications_service/
  frontend/
```

Каждый `*_service`:

- `app/main.py` — код FastAPI + CORS
- `tests/` — unit-тесты
- `requirements.txt`
- `Dockerfile`

`frontend/`:

- `app/main.py` — фронтенд-сервер
- `templates/index.html` — страница
- `static/styles.css`, `static/main.js` — стили и логика

## 2. Быстрый запуск через Docker

### Предусловия

- Установлен **Docker**
- Есть **docker compose** (в новых Docker Desktop встроен; в старых — `docker-compose`)

### Шаг 1. Распаковать архив

```bash
unzip microservices_shop_fixed.zip
cd microservices_shop_fixed
```

### Шаг 2. Поднять все сервисы

```bash
docker compose up --build
# или, если у тебя старая версия:
# docker-compose up --build
```

Docker:

- соберёт образ для каждого сервиса (по его Dockerfile)
- запустит контейнеры с портами:

| Сервис          | Порт          |
|-----------------|--------------|
| frontend        | 8000:8000    |
| users_service   | 8001:8000    |
| products_service| 8002:8000    |
| orders_service  | 8003:8000    |
| inventory       | 8004:8000    |
| payments        | 8005:8000    |
| notifications   | 8006:8000    |

### Шаг 3. Открыть в браузере

- Фронтенд: **http://localhost:8000**

Отдельные сервисы (Swagger UI):

- Users: `http://localhost:8001/docs`
- Products: `http://localhost:8002/docs`
- Orders: `http://localhost:8003/docs`
- Inventory: `http://localhost:8004/docs`
- Payments: `http://localhost:8005/docs`
- Notifications: `http://localhost:8006/docs`

### Шаг 4. Остановка

В той же папке:

```bash
docker compose down
# или docker-compose down
```

## 3. Как работает фронтенд

Файл `frontend/static/main.js` использует такие базовые URL:

```js
const USERS_BASE = "http://localhost:8001";
const PRODUCTS_BASE = "http://localhost:8002";
const ORDERS_BASE = "http://localhost:8003";
const INVENTORY_BASE = "http://localhost:8004";
const PAYMENTS_BASE = "http://localhost:8005";
const NOTIFICATIONS_BASE = "http://localhost:8006";
```

То есть, когда ты открываешь `http://localhost:8000`:

- браузер загружает HTML/JS со фронтенда;
- JS из браузера делает запросы напрямую на:
  - `http://localhost:8001/users`
  - `http://localhost:8002/products`
  - и т.д.

Во всех микросервисах включён CORS:

```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Поэтому браузер больше не блокирует запросы и **ошибка `Failed to fetch` исчезает**.

## 4. Запуск БЕЗ Docker (локально, вручную)

Если хочешь запускать всё из командной строки:

### Шаг 1. Создай виртуальное окружение (один раз)

```bash
cd microservices_shop_fixed
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### Шаг 2. Для каждого сервиса установить зависимости и запустить

Открой **несколько терминалов** или по очереди:

#### users_service (порт 8001)

```bash
cd users_service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

#### products_service (порт 8002)

```bash
cd ../products_service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

#### orders_service (порт 8003)

```bash
cd ../orders_service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003
```

#### inventory_service (порт 8004)

```bash
cd ../inventory_service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8004
```

#### payments_service (порт 8005)

```bash
cd ../payments_service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8005
```

#### notifications_service (порт 8006)

```bash
cd ../notifications_service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8006
```

#### frontend (порт 8000)

```bash
cd ../frontend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

После этого фронтенд будет доступен по `http://localhost:8000`, и он сможет общаться со всеми микросервисами (CORS уже настроен).

## 5. Unit-тесты

В каждом сервисе есть свои тесты в папке `tests/`.

Пример — `users_service/tests/test_users.py`:

- проверяет, что `GET /users` возвращает хотя бы демо-пользователя;
- проверяет, что `POST /users` создаёт пользователя.

### Как запустить тесты

Для конкретного сервиса:

```bash
cd microservices_shop_fixed/users_service
pip install -r requirements.txt
pytest
```

Аналогично:

```bash
cd ../products_service && pytest
cd ../orders_service && pytest
cd ../inventory_service && pytest
cd ../payments_service && pytest
cd ../notifications_service && pytest
```

## 6. Кратко: что ты показываешь в лабе/проекте

- Был монолит → сделали отдельные микросервисы:
  - Users, Products, Orders, Inventory, Payments, Notifications.
- Каждый сервис:
  - отдельный FastAPI-приложение
  - своё API
  - свой Dockerfile
  - свои тесты.
- Фронтенд — отдельный сервис, который ходит к ним по HTTP.
- CORS настроен корректно → фронтенд общается со всеми сервисами без `Failed to fetch`.
- docker-compose поднимает всю систему одной командой.

