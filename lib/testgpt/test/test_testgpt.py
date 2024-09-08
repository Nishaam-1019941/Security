import sys
from pathlib import Path

import openai
import pytest


sys.path.append(str(Path(__file__).parent.parent))
from testgpt import TestGPT


def test_init():
    fake_api_key = "123"
    test_gpt = TestGPT(fake_api_key)


def test_empty_open_question():
    fake_api_key = "123"
    test_gpt = TestGPT(fake_api_key)
    with pytest.raises(ValueError):
        test_gpt.generate_open_question("")


def test_empty_multiple_choice_question():
    fake_api_key = "123"
    test_gpt = TestGPT(fake_api_key)
    with pytest.raises(ValueError):
        test_gpt.generate_multiple_choice_question("")


def test_open_question(monkeypatch, mock_openai_open_create):
    fake_api_key = "123"
    test_gpt = TestGPT(fake_api_key)
    response = test_gpt.generate_open_question("YEAS")
    assert "This is your question" in response


def test_multiple_choice_question(monkeypatch, mock_openai_multiple_create):
    fake_api_key = "123"
    test_gpt = TestGPT(fake_api_key)
    response = test_gpt.generate_multiple_choice_question("YEAS")
    assert "A) Bossen" in response
