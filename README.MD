# Тестовое задание для компании TEO
Стек технологий: Python 3, Aiogram, Asyncio, Postgres, Docker

[Демонстрация бота](https://t.me/teo_test_moonrock_bot)

### Описание:
Бот взаимодействует с пользователем следуюзим образом:
- Пользователь отправляет боту команду /start (или нажимает кнопку "Начать")
- Бот приветствует пользователя и просит отправить своё имя ответным сообщением
- Пользователь отправляет боту своё имя
- Бот запрашивает у пользователя интересуующий его вопрос
- Пользователь отправляет боту свой вопрос
- Данные о пользователе сохраняются в БД
- Раз в день в 17:00 (МСК) бот отправляет пользователю сообщение с количеством дней, прошедших с регистрации

#### TODO:
- [x] Реализовать интеграцию с OpenAI API что бы бот мог отвечать на заданный пользователем вопрос


### Как запустить проект:  

#### 1. для разработки:  

```shell
git clone https://github.com/m00nrock/teo_test_task.git  
```



Заполнените .env файл:
В корневой директории создайте .env файл и укажите значения для переменных окружения:
Пример заполнения доступен в файле .env.example

- DB_NAME
- POSTGRES_USER
- POSTGRES_PASSWORD
- DB_HOST
- DB_PORT
- TOKEN
  
Создать и активировать виртуальное окружение:  
  
```shell
python -m venv venv  
```
  
```shell
source venv/bin/activate  
```
  
```shell
python -m pip install --U pip  
```
  
Установить зависимости из файла requirements.txt:  
  
```shell
pip install -r requirements.txt  
```

Запустить базу данных:
  
```shell
docker-compose -f docker-compose.dev.yaml up
```

В файле main.py изменить строку подключения к БД

```python
URI = (f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:'
       f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("LOCAL_DB")}:{os.getenv("DB_PORT")}'
       f'/{os.getenv("DB_NAME")}')
```

Запустить проект:  
  
```shell
python main.py  
```

#### 2. запуск проекта в контейнерах:
Для запуска потребуется Docker. [Get Docker](https://docs.docker.com/get-docker/)

Убедитесь, что строка подключения к БД в файле main.py указывает на контейнер с БД

```python
URI = (f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:'
       f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}'
       f'/{os.getenv("DB_NAME")}')
```

Запустите проект:
```
docker-compose up -d --build
```
