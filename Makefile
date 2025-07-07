DC=docker compose
APP_COMPOSE = --file compose/app.yaml
POSTGRES_COMPOSE = --file compose/postgres.yaml
NGINX_COMPOSE = --file compose/nginx.yaml
COMPOSE_FILES = ${APP_COMPOSE}  ${POSTGRES_COMPOSE} ${NGINX_COMPOSE}
ENV_FILE = --env-file .env.example

.PHONY: test clean all postgres app

app:
		${DC} \
		${ENV_FILE} \
		${COMPOSE_FILES}\
		up \
		--build


postgres: 
		${DC} \
		${ENV_FILE} \
		${POSTGRES_COMPOSE}\
		up
