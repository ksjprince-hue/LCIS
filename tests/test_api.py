from fastapi.testclient import TestClient

from main import app
from routers import analysis


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analysis_endpoint_preserves_response_shape(monkeypatch):
    monkeypatch.setattr(
        analysis,
        "analyze_with_llm",
        lambda source_code, ast_result: {
            "success": True,
            "response": "분석 완료",
        },
    )

    response = client.post(
        "/analysis/ast",
        json={
            "source_code": "import os\n\ndef greet(name):\n    if name:\n        return name\n",
            "filename": "sample.py",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "filename": "sample.py",
        "total_lines": 6,
        "complexity_score": 3,
        "functions": [
            {
                "name": "greet",
                "lineno": 3,
                "args": ["name"],
                "is_async": False,
                "complexity": 2,
            }
        ],
        "classes": [],
        "imports": ["os"],
        "errors": [],
        "llm_analysis": "분석 완료",
        "llm_error": "",
    }


def test_analysis_endpoint_rejects_empty_source():
    response = client.post(
        "/analysis/ast",
        json={"source_code": "   ", "filename": "empty.py"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "source_code가 비어있어요"}


def test_analysis_endpoint_keeps_llm_failure_in_response(monkeypatch):
    monkeypatch.setattr(
        analysis,
        "analyze_with_llm",
        lambda source_code, ast_result: {
            "success": False,
            "error": "Ollama unavailable",
        },
    )

    response = client.post(
        "/analysis/ast",
        json={"source_code": "value = 1", "filename": "sample.py"},
    )

    assert response.status_code == 200
    assert response.json()["llm_analysis"] == ""
    assert response.json()["llm_error"] == "Ollama unavailable"
