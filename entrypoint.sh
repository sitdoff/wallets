#!/bin/bash
# Устанавливаем строгий режим
set -e

# Ожидание доступности базы данных
bash ./wait-for-it.sh postgres:5432 -- echo "PostgreSQL is ready"
alembic upgrade head
# Запуск вашего приложения
exec "$@"
