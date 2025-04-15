# Физический тренажер

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.0-brightgreen.svg)](https://djangoproject.com)
Pylint запускался локально, полный отчёт в корне проекта: Your code has been rated at 9.01/10

Проект для оттачивания навыков решения задач по физике через интерактивные тесты. Включает систему добавления задач по разным разделам и возможность выбора тематики тестов.

## Особенности

- Возможность проходить тесты по разным разделам
- Возможность добавлять задачи в базу данных
- Детальное пояснение результатов теста
- Приятный современный дизайн
- Автоматическая проверка кода (Pylint + GitHub Actions)

## Технологии

- Python 3.9+
- Django 4.0+
- Bootstrap 5
- Pylint + pylint-django

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/TickleMeLoris/physics_trainer.git
cd physics_trainer
```
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Настройте базу данных:
```bash
python manage.py migrate
```
4. Запустите сервер:
```bash
python manage.py runserver
```
