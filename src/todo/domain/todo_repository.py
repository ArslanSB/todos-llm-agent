from abc import ABC, abstractmethod
from uuid import UUID

from todo.domain.todo import Todo


class TodoRepository(ABC):
  @abstractmethod
  async def create_todo(self, todo: Todo) -> Todo:
    raise NotImplementedError()

  @abstractmethod
  async def get_all_todos(self) -> list[Todo]:
    raise NotImplementedError()

  @abstractmethod
  async def get_all_todos_by_user_id(self, user_id: UUID) -> list[Todo]:
    raise NotImplementedError()

  @abstractmethod
  async def get_todo_by_id(self, todo_id: UUID) -> Todo | None:
    raise NotImplementedError()

  @abstractmethod
  async def update_todo(self, todo: Todo) -> Todo:
    raise NotImplementedError()

  @abstractmethod
  async def delete_todo(self, todo_id: UUID) -> None:
    raise NotImplementedError()
