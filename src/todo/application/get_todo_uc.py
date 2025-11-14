from uuid import UUID

from todo.domain.todo import Todo
from todo.domain.todo_repository import TodoRepository


class GetTodoUC:
  def __init__(self, todo_repository: TodoRepository):
    self.todo_repository = todo_repository

  async def execute(self, todo_id: UUID, user_id: UUID) -> Todo:
    todo = await self.todo_repository.get_todo_by_id(todo_id)
    if not todo or not todo.is_owned_by(user_id):
      raise ValueError("Todo not found")

    return todo
