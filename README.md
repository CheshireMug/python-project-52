## Description
Task Manager is a task management system similar to http://www.redmine.org/. It allows you to create tasks, assign performers, and change their statuses. Registration and authentication are required to use the system

### Link to the website
https://python-project-52-ukjn.onrender.com/

### Instructions for local deploying a project
1. Install Python 3.10 or higher
2. Install the uv package manager
3. Clone the created project repository locally
4. Run the make build command

### Environment variables
The project uses environment variables for configuration.  
Create a `.env` file in the root directory before running the project.

Variables and descriptions:
SECRET_KEY - Django secret key 
DEBUG - Debug mode (`True` or `False`)
DATABASE_URL - Database connection URL 
ROLLBAR_ACCESS_TOKEN - Rollbar error tracking access token

## Описание
Task Manager – система управления задачами, подобная http://www.redmine.org/. Она позволяет ставить задачи, назначать исполнителей и менять их статусы. Для работы с системой требуется регистрация и аутентификация

### Ссылка на сайт
https://python-project-52-ukjn.onrender.com/

### Инструкция по разворачиванию проекта
1. Установите Python версии 3.10 или выше
2. Установите пакетный менеджер uv
3. Клонируйте созданный репозиторий проекта локально
4. Запустите команду make build

### Переменные окружения
Проект использует переменные окружения для конфигурации.  
Перед запуском создайте файл `.env` в корневой директории проекта.

Названия переменных и описания:
SECRET_KEY - Секретный ключ Django
DEBUG - Режим отладки (`True` или `False`)
DATABASE_URL - URL подключения к базе данных
ROLLBAR_ACCESS_TOKEN - Токен для сервиса отслеживания ошибок Rollbar

### Hexlet tests and linter status:
[![Actions Status](https://github.com/CheshireMug/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/CheshireMug/python-project-52/actions)
