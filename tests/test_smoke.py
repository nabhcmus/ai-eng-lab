import ai_eng_lab


def test_import():
    assert ai_eng_lab is not None


def test_slugify_normalizes_words():
    assert ai_eng_lab.slugify("Hello, World!") == "hello-world"


def test_slugify_removes_accents_and_collapses_separators():
    assert ai_eng_lab.slugify("  Café -- déjà vu  ") == "cafe-deja-vu"


def test_slugify_returns_empty_for_non_word_text():
    assert ai_eng_lab.slugify("!!!") == ""
