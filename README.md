This is a reciept analysis webapp

activate venv -> source .venv/bin/activate
deactivate venv -> deactivate

to run -> python3 -m app.utils.main

#gpt generated file structure
'''
your_app/
├─ app/
│  ├─ __init__.py          # app factory; registers blueprints, extensions
│  ├─ config.py            # Base/Dev/Prod/Test configs
│  ├─ extensions.py        # db, migrate, (cache, jwt, etc.)
│  ├─ * utils/
│  │  └─ funcs.py
│  ├─ * models/
│  │  ├─ __init__.py
│  │  └─ user.py
│  ├─ views/               # or "api" if building a JSON API
│  │  ├─ __init__.py
│  │  └─ routes.py
│  ├─ services/            # business logic (optional)
│  ├─ schemas/             # marshmallow / pydantic (optional)
│  ├─ templates/           # Jinja templates (optional)
│  └─ static/              # CSS/JS/assets (optional)
├─ migrations/             # created by Flask-Migrate (Alembic)
├─ tests/
│  ├─ __init__.py
│  ├─ conftest.py          # pytest fixtures (app, db)
│  └─ test_health.py
├─ .env                    # local env vars (DATABASE_URL, SECRET_KEY, etc.)
├─ .env.example            # safe template of required env vars
├─ .flaskenv               # FLASK_APP, FLASK_ENV for `flask run` (optional)
├─ Dockerfile              # app container (optional)
├─ docker-compose.yml      # Postgres + app (optional but handy)
├─ Makefile                # quality-of-life commands (optional)
├─ requirements.txt        # or pyproject.toml if you prefer Poetry
├─ run.py                  # simple entrypoint (or use `flask run`)
└─ README.md
'''