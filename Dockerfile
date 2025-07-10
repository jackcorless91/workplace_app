FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG FLASK_ENV=production
ARG DATABASE_URI
ARG SECRET_KEY

ENV FLASK_ENV=${FLASK_ENV}
ENV DATABASE_URI=${DATABASE_URI}
ENV SECRET_KEY=${SECRET_KEY}

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:create_app()"]
