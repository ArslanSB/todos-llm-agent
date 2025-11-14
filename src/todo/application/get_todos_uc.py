from uuid import UUID

from todo.domain.todo_repository import TodoRepository


class GetTodosUC:
  def __init__(self, todo_repository: TodoRepository):
    self.todo_repository = todo_repository

  def execute(self, user_id: UUID):
    return self.todo_repository.get_all_todos_by_user_id(user_id=user_id)
