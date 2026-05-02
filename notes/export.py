from typing import Optional
from notes.model import Note
from notes.store import NoteStore


def export_note(note: Note) -> str:
    date_str = note.created_at.strftime("%Y-%m-%d %H:%M")
    if note.tags:
        meta = f"_Tags: {', '.join(note.tags)}_ | _Created: {date_str}_"
    else:
        meta = f"_Created: {date_str}_"

    return f"# {note.title}\n\n{meta}\n\n{note.content}"


def export_store(store: NoteStore, query: Optional[str] = None) -> str:
    notes = store.search(query) if query else store.list()
    if not notes:
        return ""
    sections = [export_note(n) for n in notes]
    return "\n\n---\n\n".join(sections)
