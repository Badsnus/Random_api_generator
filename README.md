Random API Generator
---

### Про проект:

Rest api проект для получение рандомных данных. Так как у меня есть знакомый
начинающий фронтендер и ему постоянно нужен какой-нибудь апи, чтобы получать
данный,
то я решил сделать такую штуку, которая позволяет получать данные.

Проект написан на python + fastapi + asyncpg + pickle

Методы API
---

###

Параметры get запросов для апи:

#### Fields - поля записей

fields=поля через запятую

Доступные поля:[
'id', 'user_id', 'title', 'description', 'content', 'price', 'url', 'data', 'is_published', 'status']

Пример использования: **GET list/?fields=id,title,status**

#### Offset - сдвиг записей

offset=число

Пример использования: **GET list/?offset=1

#### Limit - определенное кол-во записей

limit=число

Пример использования: **GET list/?limit=1

### GET list/

Получение списка записей из бд

Максимум можно получить 300 записей за один запрос.

### POST list/

Фейковое создание нового айтема

### GET list/{id}/

Получение информации об одной записи

### PUT list/{id}/

Фейк обновление информации об одной записи

### DELETE list/{id}/

Фейк удаление информации об одной записи


Инструкция по установке
---

#### 1)Клонируем репозиторий

    git clone https://github.com/Badsnus/Random_api_generator

#### 2)Создаем виртуальное окружение и активируем его

    python -m venv venv

    Windows: venv\Scripts\activate.bat
    Linux и MacOS: source venv/bin/activate

#### 3)Заходим в директорию репозитория

    cd Random_api_generator

#### 4) Устанавливаем зависимости

    pip install -r requirements.txt

#### 5) .env.example -> .env

    Eсть файл .env.example его нужно переименовать в .env

#### 6) Start

    uvicorn main:app



