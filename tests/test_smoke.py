import os
import pytest
from knowledge_base import KnowledgeBase

@pytest.fixture
def temp_kb(tmp_path):
    db_file = tmp_path / "test_memory.db"
    return KnowledgeBase(db_path=str(db_file))

def test_kb_smoke(temp_kb):
    # 1. Example storage
    temp_kb.remember("The capital of France is Paris.")
    temp_kb.remember("The sun is a star.")

    # 2. Retrieval and top expected answers
    response = temp_kb.respond("What is the capital of France?")
    assert "Paris" in response.message
    assert response.confidence > 0.5

    response = temp_kb.respond("What is the sun?")
    assert "star" in response.message
    assert response.confidence > 0.5

    # 3. Threshold behavior
    temp_kb.set_similarity_threshold(0.9)
    response = temp_kb.respond("Something completely unrelated about elephants")
    # With a high threshold, it should not return the near matches as valid answers
    assert "No relevant information found" in response.message

    # 4. Forget behavior
    temp_kb.set_similarity_threshold(0.3)
    temp_kb.forget("The sun is a star.")
    response = temp_kb.respond("What is the sun?")
    # It might still find "Paris" as the nearest match if it's very small KB,
    # but "The sun is a star" should be gone.
    assert "The sun is a star." not in response.message
