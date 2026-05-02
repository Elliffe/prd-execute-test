import tempfile
from datetime import datetime
from notes.model import Note
from notes.store import NoteStore
from notes.export import export_note, export_store


def make_note(title="Test Note", content="Some content", tags=None):
    return Note(
        title=title,
        content=content,
        tags=tags or [],
        created_at=datetime(2024, 3, 15, 10, 30),
    )


def test_export_note_contains_title_as_h1():
    n = make_note(title="My Note")
    md = export_note(n)
    assert "# My Note" in md


def test_export_note_contains_content():
    n = make_note(content="Hello world")
    md = export_note(n)
    assert "Hello world" in md


def test_export_note_contains_tags():
    n = make_note(tags=["python", "tips"])
    md = export_note(n)
    assert "python" in md
    assert "tips" in md


def test_export_note_contains_date():
    n = make_note()
    md = export_note(n)
    assert "2024-03-15" in md


def test_export_note_no_tags_still_renders():
    n = make_note(tags=[])
    md = export_note(n)
    assert "# " in md
    assert n.content in md


def test_export_store_contains_all_notes():
    path = tempfile.mktemp(suffix=".json")
    store = NoteStore(path)
    store.add(make_note(title="Note A", content="aaa"))
    store.add(make_note(title="Note B", content="bbb"))
    md = export_store(store)
    assert "Note A" in md
    assert "Note B" in md


def test_export_store_with_query_filters():
    path = tempfile.mktemp(suffix=".json")
    store = NoteStore(path)
    store.add(make_note(title="Python tips", content="list comprehensions"))
    store.add(make_note(title="Shopping", content="eggs and milk"))
    md = export_store(store, query="Python")
    assert "Python tips" in md
    assert "Shopping" not in md


def test_export_store_separates_notes():
    path = tempfile.mktemp(suffix=".json")
    store = NoteStore(path)
    store.add(make_note(title="A"))
    store.add(make_note(title="B"))
    md = export_store(store)
    assert "---" in md
