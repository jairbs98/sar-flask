FROM python:3.12-alpine

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP app:create_app()
ENV FLASK_ENV dev
CMD ["python", "app.py"]
