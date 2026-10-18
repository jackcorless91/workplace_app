FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG FLASK_ENV=production

ENV FLASK_ENV=${FLASK_ENV}
ENV FLASK_APP=app

# DATABASE_URI and SECRET_KEY are supplied at runtime (docker run -e ...),
# not baked into the image. If DATABASE_URI is unset, app.py falls back to sqlite.

EXPOSE 8080

# Create tables on boot (db.create_all is idempotent), then start gunicorn.
CMD ["sh", "-c", "flask db create && exec gunicorn -w 4 -b 0.0.0.0:8080 'app:create_app()'"]
