from uuid import UUID

from todo.domain.todo import Todo
from todo.domain.todo_repository import TodoRepository


class UpdateTodoUC:
  def __init__(self, todo_repository: TodoRepository):
    self.todo_repository = todo_repository

  async def execute(
    self, todo_id: UUID, title: str | None, description: str | None, completed: bool | None, user_id: UUID
  ) -> Todo:
    todo = await self.todo_repository.get_todo_by_id(todo_id)
    if not todo or not todo.is_owned_by(user_id):
      raise ValueError("Todo not found")

    if title is not None:
      todo.update_title(title)
    if description is not None:
      todo.update_description(description)
    if completed is not None:
      if completed:
        todo.mark_completed()
      else:
        todo.mark_incomplete()

    result = await self.todo_repository.update_todo(todo)

    return result
