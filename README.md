# FastApi проект с менеджером задач и конвертером валют

## Особенности
  - Создание пользователей с различными ролями(С помощью JWT Cookies)
  - Полностью асинхронный проект
     - Конечные точки
     - Тесты
     - База данных(SQLite)
     - Миграции
     - Обращение к внешним ресурсам
     - И т.д
  - Websocket сообщения при действиях, связанных с задачами
  - Пользовательский логгер

## Запуск
  1. Единственное, что вам нужно сделать - изменить API_KEY в .env, остальное всё настроено и готово к запуску
  2. Используйте в cmd: 
```bash
git clone https://github.com/DownKAX/currency_and_task_websocket.git
```
  3. **(Обязательно)** Активировать виртуальную среду
```bash
.venv\Scripts\activate
```
  4. Проект можно запустить либо запустив файл main.py, либо через:
```bash
bash uvicorn main:app --reload
```

## Тестирование
Для запуска тестов достаточно ввести 
```bash
pytest -v
```
Тесты используют отдельную тестовую базу данных, использующую миграции перед каждым тестом для изоляции. Миграции общие для тестовой и основной БД(применяются отдельно).

## Миграции
Для применения миграций к основной БД используются стандартные комманды
```bash
alembic upgrade head
alembic downgrade base
```
Если необходимо применить миграции к тестовой БД, то следует использовать следующие комманды
```bash
alembic -c alembic_test.ini upgrade head 
alembic -c alembic_test.ini downgrade base
```
## Запросы API
### Общие рекомендации
- Для аутентификации используйте `session_token`, полученный после входа (`/auth/login`). 
- В Postman: после входа перейдите в Cookies → Manage Cookies, чтобы проверить наличие `session_token`.
- Для WebSocket: используйте вкладку "WebSocket" в Postman.

---

### Аутентификация

#### 1. Регистрация
- **Метод:** POST  
- **URL:** `/auth/register`  
- **Тело запроса (JSON):**
  ```json
  {
    "username": "ваш_логин",
    "password": "ваш_пароль"
  }
  ```

---

#### 2. Вход
- **Метод:** POST  
- **URL:** `/auth/login`  
- **Тело запроса (form-data):**
  - Ключ: `username` → Значение: ваш логин.
  - Ключ: `password` → Значение: ваш пароль.
- **Ответ:** Устанавливает куку `session_token`. Используйте её для остальных запросов.

---

### Валюты

#### 3. Получить коды валют
- **Метод:** GET  
- **URL:** `/currency/get_currency_codes`  
- **Куки:** `session_token` (обязательно).  
- **Ответ:** 
  ```json
  {
    "currencies": ["USD", "EUR", "JPY", ...]
  }
  ```

---

#### 4. Конвертировать валюту
- **Метод:** POST  
- **URL:** `/currency/convert`  
- **Куки:** `session_token`.  
- **Тело запроса (JSON):**
  ```json
  {
    "amount": 100,
    "currency_code1": "USD",
    "currency_code2": "EUR"
  }
  ```
- **Ответ:** 
  ```json
  {
    "message": "100 of USD is 93.5 of EUR"
  }
  ```

---

### Задачи

#### 5. Общий чат (WebSocket)
- **Тип:** WebSocket  
- **URL:** `/tasks/general_chat`  
- **Куки:** `session_token`.  
- **Использование:** Отправляйте текстовые сообщения через подключение.

---

#### 6. Создать задачу
- **Метод:** POST  
- **URL:** `/tasks/create_task`  
- **Куки:** `session_token`.  
- **Тело запроса (JSON):**
  ```json
  {
    "title": "Название задачи",
    "description": "Описание задачи"
  }
  ```
- **Ответ:** Данные созданной задачи.

---

#### 7. Удалить задачу
- **Метод:** DELETE  
- **URL:** `/tasks/delete_task`  
- **Куки:** `session_token`.  
- **Параметр (query):** `id` → ID задачи.  
- **Пример:** `/tasks/delete_task?id=1`  
- **Ответ:** Данные удалённой задачи.

---

#### 8. Обновить задачу
- **Метод:** PUT  
- **URL:** `/tasks/update_task`  
- **Куки:** `session_token`.  
- **Параметр (query):** `id` → ID задачи.  
- **Тело запроса (JSON):** Любые поля для обновления (например, `title`, `description`).  
  ```json
  {
    "title": "Новое название"
  }
  ```
- **Ответ:** Обновлённые данные задачи.

---

#### 9. Завершить задачу
- **Метод:** PUT  
- **URL:** `/tasks/finish_task`  
- **Куки:** `session_token`.  
- **Параметр (query):** `id` → ID задачи.  
- **Пример:** `/tasks/finish_task?id=1`  
- **Ответ:** Данные задачи с датой завершения и исполнителем.

```
