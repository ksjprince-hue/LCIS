import os


def get_codebert_model_path(default: str) -> str:
    """Return the configured checkpoint path while preserving script defaults."""
    return os.getenv("CODEBERT_MODEL_PATH", default)
