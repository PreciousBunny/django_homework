# django_homework

## Описание проекта
Поэтапное создание учебного веб-приложения - интернет-магазина "SkyStore".

## Развертывание проекта
Для корректной работы проекта, вам необходимо выполнить следующие шаги:

1) Установить локально на свой компьютер Python версией не ниже 3.10.x!
2) Клонировать файлы проекта с GitHub репозитория.
3) Установите виртуальное окружение.
```bash
python -m venv venv 
```
4) Активировать виртуальное окружение (если есть необходимость).
```bash
venv/Scripts/activate.bat 
```
5) Установить необходимые зависимости проекта, указанные в файле `requirements.txt`
```bash
pip install -r requirements.txt
```
6) Установить Redis, глобально себе на компьютер (используйте wsl, терминал Ubuntu).
```bash
sudo apt-get install redis-server
```
7) Запустить Redis-сервер (Redis-сервер запустится на стандартном порту 6379).
```bash
sudo service redis-server start
```
8) Убедиться, что Redis-сервер работает правильно, выполните команду:
```bash
redis-cli ping
```
9) Установить БД PostreSQL (используйте wsl, терминал Ubuntu).
```bash
sudo apt-get install postgresql
```
10) Если БД PostreSQL уже была ранее установлена, то перезапустите сервер PostreSQL.
```bash
sudo service postgresql restart
```
11) Выполнить вход.
```bash
sudo -u postgres psql
```
12) Создать базу данных с помощью следующей команды:
```bash
create database catalog;
```
Если такая база данных уже используется, то возможно изменить ее название на свою.

13) Выйти.
```bash
\q
```
14) Создать файл .env
15) Добавить в файл настройки, как в .env.sample и заполнить их.
15) Применить миграции (локально, у себя в виртуальном окружении проекта).
```bash
python manage.py migrate
```
16) Загрузить данные JSON-файлов в созданные таблицы БД с помощью фикстур:
```bash
python manage.py loaddata data_category.json
```
```bash
python manage.py loaddata data_product.json
```
17) Запустить сервер (появившуюся ссылку открыть в браузере  http://127.0.0.1:8000/ )
```bash
python manage.py runserver
```

