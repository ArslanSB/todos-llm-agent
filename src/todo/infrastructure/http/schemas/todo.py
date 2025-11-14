from uuid import UUID

from pydantic import BaseModel, Field

from todo.domain.todo import Todo as TodoDomain


class Todo(BaseModel):
  id: UUID = Field(..., description="The unique identifier of the todo item")
  title: str = Field(..., description="The title of the todo item")
  description: str = Field(..., description="The description of the todo item")
  completed: bool = Field(..., description="The completion status of the todo item")
  user_id: UUID = Field(..., description="The unique identifier of the user who owns the todo item")
  created_at: str = Field(..., description="The creation timestamp of the todo item in ISO 8601 format")
  updated_at: str = Field(..., description="The last updated timestamp of the todo item in ISO 8601 format")
  completed_at: str | None = Field(
    ..., description="The completion timestamp of the todo item in ISO 8601 format, if completed"
  )

  @classmethod
  def from_domain(cls, todo_domain: TodoDomain) -> "Todo":
    return cls(
      id=todo_domain.id,
      title=todo_domain.title.value,
      description=todo_domain.description.value,
      completed=todo_domain.completed,
      user_id=todo_domain.user_id,
      created_at=todo_domain.created_at.isoformat(),
      updated_at=todo_domain.updated_at.isoformat(),
      completed_at=todo_domain.completed_at.isoformat() if todo_domain.completed_at else None,
    )
