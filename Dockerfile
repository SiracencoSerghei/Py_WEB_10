
FROM python:3.11

# Встановимо змінну середовища

ENV APP_HOME /app 

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

COPY run.sh run.sh

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt 

CMD ./run.sh 

