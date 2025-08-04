# 🧭 Pathfinder API

A minimal Django + DRF micro‑service for creating nodes and finding paths between them.  Includes an optional **slow** path‑finder executed asynchronously with Celery.

---

## Endpoints

| Purpose                | Method & Path                    | Notes                                                                |
| ---------------------- | -------------------------------- | -------------------------------------------------------------------- |
| Create / link a node   | **POST** `/app/node/`            | body `{ "name": "A", "child": "B" }` *(child optional)*              |
| Fast path‑finding      | **GET**  `/app/path/`            | query `?FromNode=A&ToNode=C` → `{"path": ["A","B","C"]}` or `null`   |
| Start slow path‑finder | **POST** `/app/path/slow`        | body `{ "FromNode": "A", "ToNode": "C" }` → returns `task_id`        |
| Poll slow result       | **GET**  `/app/path/slow-result` | query `?task_id=<id>` → 202 while running, 200 with result when done |

---

## Run locally (no Docker)

```bash
pip install -r requirements.txt
python manage.py migrate && python manage.py runserver
```

If you need async tasks:

```bash
celery -A PathfinderApi worker -l info   # broker defaults to redis://localhost:6379/0
```

---

## Tests (pytest)

Tests run Celery **synchronously** and **store results in memory**, so no Redis/RabbitMQ is required:

```bash
docker-compose -f dev.docker-compose.yml up -d db  # for the DB
pip install -r requirements-dev.txt   # pytest, pytest-django, coverage …
pytest -q                             # all green
```

---

## Quick Docker

```bash
docker-compose -f dev.docker-compose.yml up -d --build          # db, web, worker, redis
```

Web app at [http://localhost:8000/](http://localhost:8000/).

---

## Tech

- Python 3.11 · Django 4 · DRF 3.15
- Celery 5 (broker/result = Redis by default)
- PostgreSQL or SQLite (via `DATABASE_URL` env)
- Docker / Compose for one‑command dev setup

---

