FROM python:3-alpine

COPY webserver/requirements.txt /app/requirements.txt
WORKDIR /app

RUN apk update
RUN apk add --no-cache pkgconfig gcc python3-dev musl-dev mariadb-dev

RUN pip install -r requirements.txt

CMD [ "python3", "-u", "run.py" ]