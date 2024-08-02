# Docker services
PROJECT_PATH=/lunchlog/lunchlog/
PROJECT_NAME=lunchlog
APP_ALIAS=lunchlog_app
DB_ALIAS=lunchlog_db


docker-up: docker-compose-up
docker-down: docker-compose-down
docker-stop: docker-compose-stop
docker-ssh: docker-exec-ssh
docker-build: docker-compose-build


docker-build-up:
	@echo "Building and starting up..."
	docker compose up --build

docker-compose-up:
	@echo "Starting Docker..."
	docker compose up

docker-compose-build:
	@echo "Build docker images..."
	docker compose build

docker-compose-down:
	@echo "Stopping and putting containers down..."
	docker compose down --remove-orphans

docker-compose-stop:
	@echo "Stopping Docker..."
	docker compose stop

docker-exec-ssh:
	@echo "Entering bash..."
	docker exec -it $(APP_ALIAS) /bin/bash

# Django related
new-app:
	@echo "Creating a new app: $(APP_NAME)"
	docker compose run --workdir=$(PROJECT_PATH) app django-admin startapp $(APP_NAME)

superuser:
	@echo "Creating Django Superuser"
	docker compose run --workdir=$(PROJECT_PATH) app python manage.py createsuperuser

migrations:
	docker compose run --workdir=$(PROJECT_PATH) app python manage.py makemigrations

migrate:
	docker compose run --workdir=$(PROJECT_PATH) app python manage.py migrate

collectstatic:
	docker compose run --workdir=$(PROJECT_PATH) app python manage.py collectstatic

shell_plus:
	@echo "Starting Django shell.."
	docker compose run --workdir=$(PROJECT_PATH) app python manage.py shell_plus

tests:
	@echo "Starting test $(TEST)"
	docker compose run --workdir=$(PROJECT_PATH) app pytest $(TEST) --cov --cov-report term

tests-cov-report:
	@echo "Starting tests..."
	docker compose run --workdir=$(PROJECT_PATH) app pytest --cov --cov-report html

api-schema:
	@echo "Creating new API schema"
	docker compose run --workdir=$(PROJECT_PATH) app python manage.py spectacular --color --file schema.yml
