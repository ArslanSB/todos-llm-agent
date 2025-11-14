from uuid import UUID

from todo.domain.todo import Todo
from todo.domain.todo_repository import TodoRepository
from todo.domain.value_objects.description import Description
from todo.domain.value_objects.title import Title


class CreateTodoUC:
  def __init__(self, todo_repository: TodoRepository):
    self.todo_repository = todo_repository

  async def execute(self, title: str, description: str, user_id: UUID) -> Todo:
    todo = Todo(title=Title(title), description=Description(description), user_id=user_id)
    result = await self.todo_repository.create_todo(todo)

    return result
