from uuid import UUID

from todo.domain.todo_repository import TodoRepository


class DeleteTodoUC:
  def __init__(self, todo_repository: TodoRepository):
    self.todo_repository = todo_repository

  async def execute(self, todo_id: UUID, user_id: UUID) -> None:
    todo = await self.todo_repository.get_todo_by_id(todo_id)
    if not todo or not todo.is_owned_by(user_id):
      raise ValueError("Todo not found")

    await self.todo_repository.delete_todo(todo_id)
