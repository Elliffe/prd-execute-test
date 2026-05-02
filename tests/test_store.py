import os
import tempfile
from notes.model import Note
from notes.store import NoteStore


def make_store():
    tmp = tempfile.mktemp(suffix=".json")
    return NoteStore(tmp), tmp


def test_add_returns_note():
    store, _ = make_store()
    n = store.add(Note(title="Hello", content="World"))
    assert n.title == "Hello"


def test_get_returns_added_note():
    store, _ = make_store()
    n = store.add(Note(title="t", content="c"))
    assert store.get(n.id) == n


def test_get_returns_none_for_missing():
    store, _ = make_store()
    assert store.get("nonexistent") is None


def test_list_returns_all_notes():
    store, _ = make_store()
    store.add(Note(title="a", content="1"))
    store.add(Note(title="b", content="2"))
    assert len(store.list()) == 2


def test_delete_removes_note():
    store, _ = make_store()
    n = store.add(Note(title="t", content="c"))
    assert store.delete(n.id) is True
    assert store.get(n.id) is None


def test_delete_returns_false_for_missing():
    store, _ = make_store()
    assert store.delete("nonexistent") is False


def test_persistence_across_instances():
    _, path = make_store()
    s1 = NoteStore(path)
    n = s1.add(Note(title="persist", content="me"))
    s2 = NoteStore(path)
    assert s2.get(n.id) is not None
    assert s2.get(n.id).title == "persist"


def test_empty_store_on_missing_file():
    path = tempfile.mktemp(suffix=".json")
    store = NoteStore(path)
    assert store.list() == []
