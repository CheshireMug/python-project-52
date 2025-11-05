install:
	uv sync

collectstatic:
	uv run python3 manage.py collectstatic --noinput

migrate:
	uv run python3 manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi