.PHONY: db db-down api migrate revision test

## Start Postgres in the background and wait until it accepts connections
db:
	docker compose up -d --wait db

## Stop containers (data volume is kept)
db-down:
	docker compose down

## Run the API with auto-reload on http://localhost:8000
api: db
	cd api && uv run alembic upgrade head && uv run uvicorn app.main:app --reload --port 8000

## Apply pending migrations to the development database
migrate: db
	cd api && uv run alembic upgrade head

## Create a new migration from model changes: make revision m="add users table"
revision: db
	cd api && uv run alembic revision --autogenerate -m "$(m)"

## Run the whole test suite (starts Postgres if needed)
test: db
	cd api && uv run pytest
