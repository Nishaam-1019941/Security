import openai
import pytest


@pytest.fixture
def mock_openai_open_create(monkeypatch):
    def mock_ai(*args, **kwargs):
        return mock_open_response()

    monkeypatch.setattr(openai.ChatCompletion, "create", mock_ai)


def mock_open_response():
    return {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "This is your question",
                    "role": "assistant",
                },
            }
        ],
        "created": 1677664795,
        "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
        "model": "gpt-3.5-turbo-0613",
        "object": "chat.completion",
        "usage": {"completion_tokens": 17, "prompt_tokens": 57, "total_tokens": 74},
    }


@pytest.fixture
def mock_openai_multiple_create(monkeypatch):
    def mock_ai(*args, **kwargs):
        return mock_openai_multiple_response()

    monkeypatch.setattr(openai.ChatCompletion, "create", mock_ai)


def mock_openai_multiple_response():
    return {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "What is the correct answer?\n\nA) Bossen\nB) Duinen\nC) Graslanden\nD) Stedelijke gebieden",
                    "role": "assistant",
                },
            }
        ],
        "created": 1677664795,
        "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
        "model": "gpt-3.5-turbo-0613",
        "object": "chat.completion",
        "usage": {"completion_tokens": 17, "prompt_tokens": 57, "total_tokens": 74},
    }
