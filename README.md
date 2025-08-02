# 🧭 Pathfinder API

A Django-based RESTful service for creating graph nodes and finding paths between them. Includes support for asynchronous path-finding via Celery and Redis.

---

## 🚀 Features

- Create nodes and connect them in-memory
- Compute paths between nodes using BFS
- REST API endpoints using Django REST Framework
- Asynchronous path computation via Celery
- PostgreSQL-backed persistent storage
- Dockerized development environment

---

## 📦 Tech Stack

- Python 3.11
- Django 4.x
- Django REST Framework
- PostgreSQL
- Redis (for Celery broker and result backend)
- Celery
- Docker & Docker Compose

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/pathfinder-api.git
cd pathfinder-api
```

### 2. Build and Run with Docker
```bash
docker-compose up --build
```

This will:
- Start PostgreSQL and Redis
- Run migrations and load test data
- Start Django development server on `http://localhost:8000`
- Start Celery worker

---

## 🔌 REST API Endpoints

### `POST /create-node/`
Create a new graph node.
```json
{
  "name": "A"
}
```

### `GET /find-path/?FromNode=A&ToNode=C`
Returns a list of node names from A to C or `null` if no path exists.

### `POST /slow-find-path/`
Triggers asynchronous path-finding.
```json
{
  "FromNode": "A",
  "ToNode": "C"
}
```
Response:
```json
{
  "task_id": "<celery-task-id>"
}
```

### `GET /get-slow-path-result/?task_id=<id>`
Returns the status and result of the async path-finding task.

---

## 🧪 Running Tests
```bash
python manage.py test
```
Tests are located in `yourapp/tests.py` and use Django’s test framework.

---

## 🗃 Test Data
Initial nodes A → B → C are preloaded from `test_data.json` via `loaddata`.