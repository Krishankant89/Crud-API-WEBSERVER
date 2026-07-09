run:
	python run.py

migrate:
	flask db migrate -m "migration"

upgrade:
	flask db upgrade

test:
	pytest
freeze:
	pip freeze > requirements .txt