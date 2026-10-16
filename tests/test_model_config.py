from modules.model_config import get_codebert_model_path


def test_codebert_model_path_uses_default(monkeypatch):
    monkeypatch.delenv("CODEBERT_MODEL_PATH", raising=False)

    assert get_codebert_model_path("./results/checkpoint-1") == "./results/checkpoint-1"


def test_codebert_model_path_can_be_overridden(monkeypatch):
    monkeypatch.setenv("CODEBERT_MODEL_PATH", "/models/codebert")

    assert get_codebert_model_path("./results/checkpoint-1") == "/models/codebert"
