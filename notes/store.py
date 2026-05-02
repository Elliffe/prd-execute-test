import json
import os
from typing import Dict, List, Optional
from notes.model import Note
from datetime import datetime


class NoteStore:

    def __init__(self, path: str) -> None:
        self._path = path
        self._notes: Dict[str, Note] = {}
        if os.path.exists(path):
            self._load()

    def add(self, note: Note) -> Note:
        self._notes[note.id] = note
        self._save()
        return note

    def get(self, id: str) -> Optional[Note]:
        return self._notes.get(id)

    def list(self) -> List[Note]:
        return list(self._notes.values())

    def delete(self, id: str) -> bool:
        if id not in self._notes:
            return False
        del self._notes[id]
        self._save()
        return True

    def search(self, query: str) -> List[Note]:
        q = query.lower()
        return [
            n for n in self._notes.values()
            if q in n.title.lower() or q in n.content.lower()
        ]

    def filter_by_tag(self, tag: str) -> List[Note]:
        return [n for n in self._notes.values() if tag in n.tags]

    def filter_by_date(
        self,
        since: datetime,
        until: Optional[datetime] = None,
    ) -> List[Note]:
        results = [n for n in self._notes.values() if n.created_at >= since]
        if until is not None:
            results = [n for n in results if n.created_at <= until]
        return results

    def _save(self) -> None:
        data = {
            nid: {
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "tags": n.tags,
                "created_at": n.created_at.isoformat(),
            }
            for nid, n in self._notes.items()
        }
        with open(self._path, "w") as f:
            json.dump(data, f)

    def _load(self) -> None:
        with open(self._path) as f:
            data = json.load(f)
        for nid, d in data.items():
            self._notes[nid] = Note(
                id=d["id"],
                title=d["title"],
                content=d["content"],
                tags=d["tags"],
                created_at=datetime.fromisoformat(d["created_at"]),
            )
