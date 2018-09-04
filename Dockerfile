FROM jfloff/alpine-python:2.7-slim
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN apk add --update python-dev gcc mysql-dev linux-headers
RUN apk add musl-dev linux-headers
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python"]

CMD ["-m", "swagger_server"]
