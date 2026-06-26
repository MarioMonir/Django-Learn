# Django Learn

A hands-on Django learning project covering core Django patterns — from views and templates to REST APIs and testing.

## What's inside

| App | Description |
|-----|-------------|
| `ping` | Health-check endpoint |
| `todos` | REST API with Django REST Framework (serializers, viewsets) |
| `todos_v1` | Server-rendered todos with Django templates, forms, and a service layer |

## Stack

- **Django 6** — web framework
- **Django REST Framework** — REST API layer
- **pytest + pytest-django** — test runner
- **SQLite** — default dev database

## Setup

```bash
# 1. Clone
git clone https://github.com/MarioMonir/Django-Learn.git
cd Django-Learn

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements-dev.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and set DJANGO_SECRET_KEY to a strong random value

# 5. Run migrations
python manage.py migrate

# 6. Start the dev server
python manage.py runserver
```

## Running tests

```bash
pytest
# or watch mode
ptw
```

## Project structure

```
DjangoLearn/
├── DjangoLearn/          # Project config (settings, root urls, wsgi/asgi)
│   ├── ping/             # Health-check app
│   ├── todos/            # DRF REST API app
│   └── todos_v1/         # Template-based app with service layer
├── manage.py
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Dev + test dependencies
└── .env.example          # Environment variable template
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | insecure dev key | Django secret key — **must be set in production** |
| `DJANGO_DEBUG` | `true` | Set to `false` in production |
| `DJANGO_ALLOWED_HOSTS` | `localhost 127.0.0.1` | Space-separated list of allowed hosts |
