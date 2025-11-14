import datetime
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from todo.domain.value_objects.description import Description
from todo.domain.value_objects.title import Title


@dataclass
class Todo:
  title: Title
  description: Description
  user_id: UUID
  completed: bool = field(default=False)
  id: UUID = field(default_factory=uuid4)
  created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
  updated_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
  completed_at: datetime.datetime | None = None

  def is_owned_by(self, user_id: UUID) -> bool:
    return self.user_id == user_id

  def mark_completed(self) -> None:
    self.completed = True
    self.completed_at = datetime.datetime.now(datetime.timezone.utc)
    self.updated_at = datetime.datetime.now(datetime.timezone.utc)

  def mark_incomplete(self) -> None:
    self.completed = False
    self.completed_at = None
    self.updated_at = datetime.datetime.now(datetime.timezone.utc)

  def update_title(self, title: str) -> None:
    self.title = Title(title)
    self.updated_at = datetime.datetime.now(datetime.timezone.utc)

  def update_description(self, description: str) -> None:
    self.description = Description(description)
    self.updated_at = datetime.datetime.now(datetime.timezone.utc)
