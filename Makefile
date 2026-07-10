APP_NAME := crud-api-webserver
APP_VERSION ?= 1.0.0
IMAGE := $(APP_NAME):$(APP_VERSION)
CONTAINER_NAME ?= $(APP_NAME)
PORT ?= 5000
DATABASE_URL ?= sqlite:///students.db

.PHONY: run migrate upgrade test freeze docker-build docker-run docker-stop

run:
	python3 run.py

migrate:
	flask db migrate -m "migration"

upgrade:
	flask db upgrade

test:
	pytest

freeze:
	pip freeze > requirements.txt

docker-build:
	docker build -t $(IMAGE) .

docker-run:
	docker run --rm -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):5000 \
		-e PORT=5000 \
		-e DATABASE_URL=$(DATABASE_URL) \
		$(IMAGE)

docker-stop:
	docker stop $(CONTAINER_NAME)