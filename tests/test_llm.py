from types import SimpleNamespace

from ai_eng_lab.llm import ask


def make_fake_client(text: str):
    def create(**kwargs):
        msg = SimpleNamespace(content=text)
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)])

    completions = SimpleNamespace(create=create)
    return SimpleNamespace(chat=SimpleNamespace(completions=completions))


def test_ask_returns_text():
    assert ask("hi", client=make_fake_client("xin chào")) == "xin chào"
