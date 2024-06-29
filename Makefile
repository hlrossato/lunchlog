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

django-superuser: django-createsuperuser
django-new-app: django-create-new-app


docker-compose-up:
	@echo "Starting Docker..."
	@docker-compose up

docker-compose-build:
	@echo "Build docker images..."
	@docker-compose build

docker-compose-down:
	@echo "Stopping and putting containers down..."
	@docker-compose down --remove-orphans

docker-compose-stop:
	@echo "Stopping Docker..."
	@docker-compose stop

docker-exec-ssh:
	@echo "Entering bash..."
	@docker exec -it $(APP_ALIAS) /bin/bash

# Django related
django-create-new-app:
	@echo "Creating a new app: $(APP_NAME)"
	@docker-compose run --workdir=$(PROJECT_PATH) app django-admin startapp $(APP_NAME)

django-createsuperuser:
	@echo "Creating Django Superuser"
	@docker-compose run --workdir=$(PROJECT_PATH) app python manage.py createsuperuser

django-migrations:
	@docker-compose run --workdir=$(PROJECT_PATH) app python manage.py makemigrations

django-migrate:
	@docker-compose run --workdir=$(PROJECT_PATH) app python manage.py migrate

django-shell:
	@echo "Starting Django shell.."
	@docker-compose run --workdir=$(PROJECT_PATH) app python manage.py shell_plus
