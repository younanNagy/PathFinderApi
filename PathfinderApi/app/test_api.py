from __future__ import annotations

import pytest
from rest_framework import status
from rest_framework.test import APIClient



client = APIClient()


def create_node(name: str, *, child: str | None = None):
    """POST /app/node/ and return the DRF response."""
    payload = {"name": name}
    if child:
        payload["child"] = child
    return client.post("/app/node/", payload, format="json")


def find_path(source: str, target: str):
    """GET /app/path/?FromNode=A&ToNode=B – returns the DRF response."""
    return client.get("/app/path/", {"FromNode": source, "ToNode": target})


def slow_find_path(source: str, target: str):
    """POST /app/path/slow – returns the task-creation response."""
    return client.post("/app/path/slow", {"FromNode": source, "ToNode": target}, format="json")


def slow_path_result(task_id: str):
    """GET /app/path/slow-result?task_id=<id> – returns the task-result response."""
    return client.get("/app/path/slow-result", {"task_id": task_id})


@pytest.fixture(autouse=True)
def force_celery_eager(settings):
    
    if not hasattr(settings, "CELERY_TASK_ALWAYS_EAGER"):
        settings.CELERY_TASK_ALWAYS_EAGER = False
    if not hasattr(settings, "CELERY_TASK_EAGER_PROPAGATES"):
        settings.CELERY_TASK_EAGER_PROPAGATES = True


    _orig_eager = settings.CELERY_TASK_ALWAYS_EAGER
    _orig_prop  = settings.CELERY_TASK_EAGER_PROPAGATES

    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

    
    from app.celery import app as celery_app     
    _orig_app_eager = celery_app.conf.task_always_eager
    _orig_app_prop  = celery_app.conf.task_eager_propagates

    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True

    yield 


    settings.CELERY_TASK_ALWAYS_EAGER = _orig_eager
    settings.CELERY_TASK_EAGER_PROPAGATES = _orig_prop
    celery_app.conf.task_always_eager = _orig_app_eager
    celery_app.conf.task_eager_propagates = _orig_app_prop


@pytest.mark.django_db
def test_create_node_success():
    resp = create_node("A")
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.data["name"] == "A"


@pytest.mark.django_db
def test_create_node_requires_name():
    resp = client.post("/app/node/", {}, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in resp.data


@pytest.mark.django_db
def test_find_path_success():
    # A → B → C
    create_node("C")
    create_node("B",child="C")
    create_node("A",child="B")
    

    resp = find_path("A", "C")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["path"] == ["A", "B", "C"]


@pytest.mark.django_db
def test_find_path_not_found():
    create_node("X")
    resp = find_path("X", "Y")
    # Service returns 200 with path=None; adjust if you choose to return 404 instead
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["path"] is None


@pytest.mark.django_db
def test_slow_find_path_immediate_result():
    create_node("Q")
    create_node("P", child="Q")

    task_resp = slow_find_path("P", "Q")
    assert task_resp.status_code == status.HTTP_202_ACCEPTED
    task_id = task_resp.data["task_id"]

    result_resp = slow_path_result(task_id)
    assert result_resp.status_code == status.HTTP_200_OK
    assert result_resp.data["status"] == "PENDING"
