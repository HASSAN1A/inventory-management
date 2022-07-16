FROM python:3.8.5-alpine

COPY . /app
WORKDIR /app

RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base

RUN apk add netcat-openbsd
RUN apk update && apk upgrade

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


RUN chmod +x /docker-entrypoint-initdb.d/init_db.sh


CMD ["python", "manage.py", "runserver", "--host=0.0.0.0:8000"]