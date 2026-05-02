from notes.model import Note


def make_note():
    return Note(title="t", content="c")


def test_add_tag():
    n = make_note()
    n.add_tag("python")
    assert "python" in n.tags


def test_add_tag_normalises_whitespace_and_case():
    n = make_note()
    n.add_tag("  Python  ")
    assert "python" in n.tags


def test_add_tag_is_idempotent():
    n = make_note()
    n.add_tag("python")
    n.add_tag("python")
    assert n.tags.count("python") == 1


def test_remove_tag():
    n = make_note()
    n.add_tag("python")
    n.remove_tag("python")
    assert "python" not in n.tags


def test_remove_tag_noop_if_absent():
    n = make_note()
    n.remove_tag("missing")  # should not raise


def test_has_tag_true():
    n = make_note()
    n.add_tag("python")
    assert n.has_tag("python") is True


def test_has_tag_case_insensitive():
    n = make_note()
    n.add_tag("python")
    assert n.has_tag("Python") is True
    assert n.has_tag("PYTHON") is True


def test_has_tag_false():
    n = make_note()
    assert n.has_tag("absent") is False
