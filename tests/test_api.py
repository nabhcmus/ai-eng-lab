from types import SimpleNamespace

from fastapi.testclient import TestClient

from ai_eng_lab.api import app
from ai_eng_lab.llm import get_client


def make_fake_client(text: str):
    def create(**kwargs):
        msg = SimpleNamespace(content=text)
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)])

    completions = SimpleNamespace(create=create)
    return SimpleNamespace(chat=SimpleNamespace(completions=completions))


def test_health():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_extract_endpoint_returns_job_posting():
    app.dependency_overrides[get_client] = lambda: make_fake_client(
        '{"title": "AI Engineer", "skills": ["Python"]}'
    )
    try:
        response = TestClient(app).post(
            "/extract",
            json={"text": "Need an AI Engineer with Python"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["title"] == "AI Engineer"
    assert response.json()["skills"] == ["Python"]


def test_extract_endpoint_rejects_empty_text():
    response = TestClient(app).post("/extract", json={"text": ""})

    assert response.status_code == 422
