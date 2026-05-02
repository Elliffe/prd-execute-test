from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import uuid


@dataclass
class Note:
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)

    def __repr__(self) -> str:
        return f"Note(id={self.id!r}, title={self.title!r})"

    def add_tag(self, tag: str) -> None:
        normalised = tag.strip().lower()
        if normalised not in self.tags:
            self.tags.append(normalised)

    def remove_tag(self, tag: str) -> None:
        normalised = tag.strip().lower()
        if normalised in self.tags:
            self.tags.remove(normalised)

    def has_tag(self, tag: str) -> bool:
        return tag.strip().lower() in self.tags
