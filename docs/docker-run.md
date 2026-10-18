# Docker run fixes (`Dockerfile`, `app.py`, `compose.yaml`)

The image built cleanly with `docker build -t workplace_app .`, but running
it with a plain `docker run -p 8080:8080 workplace_app` failed. This document
explains what was broken, why, and how each issue was fixed in code. For how
to run the app locally, see [Running Locally](../README.md#running-locally)
in the README.

## 1. App crashed on startup with an empty `DATABASE_URI`

**Symptom:** every gunicorn worker failed to boot with:

```
sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL from string ''
```

**Cause:** `app.py` read the database URI with
`os.environ.get("DATABASE_URI", "sqlite:///test.db")`. That default is only
used when the key is **completely absent**. The Dockerfile declared
`ARG DATABASE_URI` (no default) and always set
`ENV DATABASE_URI=${DATABASE_URI}`, so with no build arg the image had
`DATABASE_URI` baked in as an *empty string* — which counts as "set" — and
SQLAlchemy was handed `''`. `SECRET_KEY` was handled the same way.

**Fix:**
- `app.py` now uses `os.environ.get("DATABASE_URI") or "sqlite:///test.db"`,
  so an empty value also falls back to sqlite.
- The Dockerfile no longer declares `ARG`/`ENV` for `DATABASE_URI` or
  `SECRET_KEY`. These are supplied at runtime (`docker run -e ...`, Compose,
  or Cloud Run env vars) instead of being baked into the image, which also
  stops secrets leaking into image layers/history.
- `dev-container.yml` no longer passes them as `--build-arg`s; it already
  passed them at runtime with `-e`.

## 2. Routes returned 500 with "no such table"

**Symptom:** once the app booted, any resource route (e.g.
`GET /team_members/`) returned a 500 with:

```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: team_members
```

**Cause:** the sqlite database was created fresh inside the container, but
table creation was only available as a manual Flask CLI command
(`flask db create` in `controllers/cli_controller.py`) and never ran.

**Fix:** the Dockerfile's `CMD` now runs `flask db create` before starting
gunicorn. `db.create_all()` only creates missing tables, so this is safe on
every boot and against Postgres in production. Seeding sample data is still
manual: `docker exec <container> flask db seed`.

## 3. Data lost whenever the container was recreated

**Cause:** the sqlite file lived in the container's writable layer.

**Fix:** `compose.yaml` mounts a named volume at `/app/instance` (where
Flask-SQLAlchemy stores the relative `sqlite:///test.db`), so data persists
across `docker compose down`/`up`. `docker compose down -v` resets it.
Plain `docker run` without a volume still starts with an empty database each
time — mount a volume or point `DATABASE_URI` at an external database if
that matters.

## Net result

`docker run -p 8080:8080 workplace_app` and `docker compose up --build` both
boot without any extra flags or `docker exec` steps. Verified all seven
resource routes (`/team_members/`, `/rosters/`, `/projects/`,
`/performance_reviews/`, `/departments/`, `/clients/`, `/client_feedbacks/`)
return `200`, and that seeded data survives a Compose `down`/`up`.
