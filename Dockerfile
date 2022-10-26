FROM python:3.10-alpine

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=0

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
