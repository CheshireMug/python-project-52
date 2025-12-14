install:
	uv sync

collectstatic:
	uv run python3 manage.py collectstatic --noinput

migrate:
	uv run python3 manage.py migrate

build:
	./build.sh

render-start:
	uv sync
	uv run gunicorn task_manager.wsgi
#	gunicorn task_manager.wsgi
