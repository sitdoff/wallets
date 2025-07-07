DC=docker compose
APP_COMPOSE = --file compose/app.yaml
DEV_APP_COMPOSE = --file compose/app-dev.yaml
POSTGRES_COMPOSE = --file compose/postgres.yaml
NGINX_COMPOSE = --file compose/nginx.yaml
DEV_COMPOSE_FILES = ${DEV_APP_COMPOSE} ${POSTGRES_COMPOSE}
COMPOSE_FILES = ${APP_COMPOSE}  ${POSTGRES_COMPOSE} ${NGINX_COMPOSE}
ENV_FILE = --env-file .env.example

.PHONY: test clean all postgres app dev

dev:
		${DC} \
		${ENV_FILE} \
		${DEV_COMPOSE_FILES} \
		up \
		--build

app:
		${DC} \
		${ENV_FILE} \
		${COMPOSE_FILES} \
		up \
		--build

postgres: 
		${DC} \
		${ENV_FILE} \
		${POSTGRES_COMPOSE}\
		up
