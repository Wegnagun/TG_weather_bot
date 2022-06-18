# TG_weather_bot
# telegram weather bot
## Описание
Бот в телеграм для ответ о погоде по запросу города

## Стек технологий:
- проект написан на Python
- библиотеки
- система управления версиями - git

## Запуск проекта
- Клонируйте репозитроий с проектом:  
`git clone https://github.com/belisnkii1/api_yatube`    

- В созданной директории установите виртуальное окружение, активируйте его и установите необходимые зависимости:  
`python3 -m venv venv`  
`. venv/bin/activate`  
`pip install -r requirements.txt`    

- Создайте в директории файл .env и поместите туда SECRET_KEY, необходимый для запуска проекта:  
*сгенерировать ключ можно на сайте Djecrety*

- Выполните миграции:

`python manage.py migrate`  

- Создайте суперпользователя:  
`python manage.py createsuperuser`  
