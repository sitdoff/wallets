[![TEST](https://github.com/sitdoff/wallets/actions/workflows/tests.yml/badge.svg)](https://github.com/sitdoff/wallets/actions/workflows/tests.yml)

# Кошельки

Api имитируещее работу с кошельками.

## Стэк

- **Фреймворк:** FastAPI
- **База данных:** PostgreSQL, SQLAlchemy, Alembic
- **HTTP-сервер:** Uvicorn, Nginx
- **Тестирование:** Pytest
- **Контейнеризация:** Docker, Docker Compose

## Развертывание

### Docker

1. Клонируем репозиторий.

```bash
git clone git@github.com:sitdoff/wallets.git
```

2. Переходим в папку проекта

```bash
cd wallets
```

3. Создаем `.env`-файл с переменными окружения.

   Это не обязательно, .env.example присутствующий в проекте тоже подходит.

```bash
cat .env.example > .env
```

4. Запускаем сборку и запуск контейнеров

```bash
docker compose \
        --env-file .env.example \
        --file compose/app.yaml \
        --file compose/postgres.yaml \
        --file compose/nginx.yaml \
        up -d \

```

```bash
#Или используем команду `make app`, если пользуетесь утилитой make.
```

Если нужен просмотр логов приложения выполните команду

```bash
docker logs wallets-app -f
```

5. Приложение по умолчанию настроено на запуск для демонстрации.

При запуске контейнера будут применены миграции.

Все приготовления выполняются в entrypoint.sh

Приложение будет доступно по адресу http://localhost:8000

Документация расположена по стандартному пути http://localhost:8000/docs

## Endpoints

Перечень эндпоинтов находятся в разворачиваемых списках.

<details>
<summary>Кошельки</summary>

---

- #### Создание кошелька

  Method: POST

  **/api/v1/wallets/create**

---

- #### Получение списка всех кошельков и их балансов.

  Method: GET

  **/api/v1/wallets/all**

---

- #### Получение баланса кошелька по его uuid.

  Method: GET

  **/api/v1/wallets/{uuid}**

---

- #### Увеличение или уменьшение баланса кошелька на заданную величину.

  Method: POST

  **/api/v1/wallets/{uuid}/operation**

  Payload:

  ```json
  {
    "operation_type": "DEPOSIT",
    "amount": 100
  }
  ```

---

</details>
