#!/usr/bin/env bash
# скачиваем uv
PYTHONPATH=.
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# здесь добавьте все необходимые команды для установки вашего проекта
# команду установки зависимостей, сборки статики, применения миграций и другие
pip3 install gunicorn
make install && make collectstatic && make migrate