## Project in progress yet

# ToDoApp
Todo App is a user-friendly web-app that helps you stay organized and manage your tasks effectively. Create an account or log in to access your personalized dashboard. From there, you can easily create tasks, set due dates, and assign priorities.

## Веб-приложение Планировщик задач

__Стек__: Python,Django,Postgres


Как запустить (установить зависимости, заполнить .env+какими значениями,
накатить миграции, запустить проект)

На локальном сервере:

1.Запустить контейнер postgres
2.Запустить django server
3.Запустить остальные контейнеры

## Requirements

* Docker version 24.0.2
* PostgreSQL 15.1-alpine
* Django 4.2.2

## Build

```bash
sudo docker-compose up --build
```