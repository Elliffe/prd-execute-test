from datetime import datetime
import uuid
from notes.model import Note


def test_note_requires_only_title_and_content():
    n = Note(title="Hello", content="World")
    assert n.title == "Hello"
    assert n.content == "World"


def test_note_id_is_auto_generated():
    n = Note(title="a", content="b")
    assert isinstance(n.id, str)
    uuid.UUID(n.id)  # raises if not a valid UUID


def test_note_ids_are_unique():
    a = Note(title="a", content="b")
    b = Note(title="a", content="b")
    assert a.id != b.id


def test_note_created_at_is_auto_set():
    before = datetime.now()
    n = Note(title="t", content="c")
    after = datetime.now()
    assert isinstance(n.created_at, datetime)
    assert before <= n.created_at <= after


def test_note_tags_default_to_empty_list():
    n = Note(title="t", content="c")
    assert n.tags == []


def test_note_tags_can_be_set():
    n = Note(title="t", content="c", tags=["python", "notes"])
    assert n.tags == ["python", "notes"]


def test_note_repr_includes_title_and_id():
    n = Note(title="My Note", content="content")
    r = repr(n)
    assert "My Note" in r
    assert n.id in r
