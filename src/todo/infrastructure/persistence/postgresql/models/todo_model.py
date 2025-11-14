from uuid import UUID

from sqlalchemy import TIMESTAMP, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from shared.infrastructure.persistence.postgresql.declarative_base import Base
from todo.domain.todo import Todo
from todo.domain.value_objects.description import Description
from todo.domain.value_objects.title import Title


class TodoModel(Base):
  __tablename__ = "todos"

  id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
  title: Mapped[str] = mapped_column(nullable=False)
  description: Mapped[str] = mapped_column(nullable=True)
  completed: Mapped[bool] = mapped_column(default=False, nullable=False)
  user_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
  created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
  updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
  completed_at: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

  def to_entity(self) -> Todo:
    return Todo(
      id=self.id,
      title=Title(self.title),
      description=Description(self.description),
      completed=self.completed,
      user_id=self.user_id,
      created_at=self.created_at,  # type: ignore
      updated_at=self.updated_at,  # type: ignore
      completed_at=self.completed_at,  # type: ignore
    )

  @classmethod
  def from_entity(cls, todo: Todo) -> "TodoModel":
    return cls(
      id=todo.id,
      title=todo.title.value,
      description=todo.description.value,
      completed=todo.completed,
      user_id=todo.user_id,
      created_at=todo.created_at,
      updated_at=todo.updated_at,
      completed_at=todo.completed_at,
    )
