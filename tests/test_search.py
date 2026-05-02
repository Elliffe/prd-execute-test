from datetime import datetime, timedelta
import tempfile
from notes.model import Note
from notes.store import NoteStore


def make_store_with_notes():
    path = tempfile.mktemp(suffix=".json")
    store = NoteStore(path)
    store.add(Note(title="Python tips", content="Use list comprehensions"))
    store.add(Note(title="Shopping list", content="Milk, eggs, PYTHON cake"))
    store.add(Note(title="Meeting notes", content="Discuss project roadmap", tags=["work"]))
    store.add(Note(title="Recipe", content="Bake at 350F", tags=["food", "cooking"]))
    return store


def test_search_matches_title():
    store = make_store_with_notes()
    results = store.search("Python")
    titles = {n.title for n in results}
    assert "Python tips" in titles


def test_search_matches_content():
    store = make_store_with_notes()
    results = store.search("list comprehensions")
    assert any("Python tips" in n.title for n in results)


def test_search_is_case_insensitive():
    store = make_store_with_notes()
    results = store.search("python")
    assert len(results) >= 2  # title and content matches


def test_search_returns_empty_for_no_match():
    store = make_store_with_notes()
    assert store.search("zzznomatch") == []


def test_filter_by_tag_returns_matching_notes():
    store = make_store_with_notes()
    results = store.filter_by_tag("work")
    assert all("work" in n.tags for n in results)
    assert len(results) == 1


def test_filter_by_tag_returns_empty_for_missing_tag():
    store = make_store_with_notes()
    assert store.filter_by_tag("nonexistent") == []


def test_filter_by_date_since():
    path = tempfile.mktemp(suffix=".json")
    store = NoteStore(path)
    old = Note(title="old", content="x", created_at=datetime(2020, 1, 1))
    new = Note(title="new", content="x", created_at=datetime(2024, 1, 1))
    store.add(old)
    store.add(new)
    results = store.filter_by_date(since=datetime(2023, 1, 1))
    titles = {n.title for n in results}
    assert "new" in titles
    assert "old" not in titles


def test_filter_by_date_range():
    path = tempfile.mktemp(suffix=".json")
    store = NoteStore(path)
    for year in [2020, 2022, 2024]:
        store.add(Note(title=str(year), content="x", created_at=datetime(year, 6, 1)))
    results = store.filter_by_date(since=datetime(2021, 1, 1), until=datetime(2023, 1, 1))
    titles = {n.title for n in results}
    assert "2022" in titles
    assert "2020" not in titles
    assert "2024" not in titles
