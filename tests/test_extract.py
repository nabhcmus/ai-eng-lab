from types import SimpleNamespace

import pytest

from ai_eng_lab.extract import JobPosting, extract


def make_fake_client(outputs: list[str]):
    calls = {"n": 0}

    def create(**kwargs):
        text = outputs[min(calls["n"], len(outputs) - 1)]
        calls["n"] += 1
        msg = SimpleNamespace(content=text)
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)])

    completions = SimpleNamespace(create=create)
    return SimpleNamespace(chat=SimpleNamespace(completions=completions))


def test_extract_valid_json():
    client = make_fake_client(['{"title": "AI Engineer", "skills": ["Python"]}'])
    result = extract("...", JobPosting, client=client)
    assert result.title == "AI Engineer"
    assert result.skills == ["Python"]


def test_extract_retries_after_invalid_json():
    client = make_fake_client(["không phải json", '{"title": "ML Engineer"}'])
    assert extract("...", JobPosting, client=client).title == "ML Engineer"


def test_extract_raises_when_always_invalid():
    client = make_fake_client(["xấu"])
    with pytest.raises(ValueError):
        extract("...", JobPosting, client=client)
