# CI workflow fixes (`.github/workflows/ci.yml`)

The initial version of the CI workflow (commit `fd184ec`, "added ci.yml, pls
work lol") failed for several unrelated reasons. This document explains what
was broken, why, and what change fixed each issue, culminating in the
current working workflow (`179431f`, "reworked ci.yml and added caching").

## 1. Deprecated `upload-artifact` action (`c70236b`)

**Problem:** the workflow used `actions/upload-artifact@v3`. GitHub
deprecated and eventually disabled `v3`, so the "Upload test results" step
failed outright regardless of whether the tests passed.

**Fix:** bumped to `actions/upload-artifact@v4`.

## 2. Virtualenv created but never used correctly across steps (`8532933`)

**Problem:** the "Install dependencies" step created a venv
(`python -m venv venv && source venv/bin/activate`) and installed packages
into it. Each GitHub Actions `run:` step executes in its own shell process,
so activating a venv in one step does not carry over to the next step —
`source venv/bin/activate` in "Run tests" started a *new* shell that had to
re-activate it. In practice this mismatch between the runner's system
Python and the venv (plus the redundant activation) caused dependency
resolution/import errors when pytest ran.

**Fix:** dropped the venv entirely and installed dependencies straight into
the runner's system Python with `pip install -r requirements.txt`. This is
safe because each CI run gets a fresh, disposable VM — there's no need to
isolate a virtualenv the way you would on a local machine.

## 3. No database configured for tests (`62f7ba2`, `3de0485`)

**Problem:** `app.py` reads `DATABASE_URI` from the environment
(`app.py:23`) and, at the time, fell back to `sqlite:///test.db` only when
the variable was completely unset (it now also falls back when it's empty —
see [docker-run.md](docker-run.md)). Nothing in the workflow set `DATABASE_URI` or created
the SQLite schema, so any test hitting the database failed — either with a
connection/URL error or with "no such table" once a URI was supplied.

**Fix, in two steps:**
- `62f7ba2` added a "Set up the database" step that exported
  `DATABASE_URI=sqlite:///test.db` and ran `flask db upgrade`, `flask db
  create`, `flask db seed`.
- `3de0485` removed `flask db upgrade` — the app has no migration
  framework (Flask-Migrate/Alembic) wired up, only the plain
  `flask db create` / `flask db seed` CLI commands defined in
  `controllers/cli_controller.py`. `flask db upgrade` isn't a real command
  here, so it errored immediately and was dropped.

## 4. Final cleanup and hardening (`179431f`)

Once the workflow was functionally passing, it was reworked for
correctness and speed:

- **Moved `DATABASE_URI` (and `FLASK_APP`, `FLASK_ENV`) to a job-level
  `env:` block** instead of `export`-ing it inline in one step. This makes
  the value available to every step (including "Run tests", which also
  touches the DB via the app config) instead of only the shell process of
  the step that exported it.
- **Added `actions/cache@v4` for `~/.cache/pip`**, keyed on the hash of
  `requirements.txt`. This isn't a correctness fix — it speeds up repeat
  runs by skipping re-downloading unchanged dependencies.
- **Renamed "Set up the database" → "Set up the test database"** for
  clarity, since `DATABASE_URI` is now scoped to this CI job's SQLite file
  and not a real environment.

## Net result

The workflow went from failing at multiple independent points (a
deprecated action, a venv that didn't persist across steps, and a database
that was never created) to a minimal, working pipeline: install deps
(cached) → create + seed a throwaway SQLite DB → run pytest → upload the
JUnit results as an artifact.
