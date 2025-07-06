FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8080

ARG FLASK_ENV=development
ENV FLASK_ENV=${FLASK_ENV}

ARG DATABASE_URI
ARG SECRET_KEY
ENV DATABASE_URI=${DATABASE_URI}
ENV SECRET_KEY=${SECRET_KEY}

EXPOSE 8080

CMD ["flask", "run"]
