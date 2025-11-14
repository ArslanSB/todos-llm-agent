from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo.domain.todo import Todo
from todo.domain.todo_repository import TodoRepository
from todo.infrastructure.persistence.postgresql.models.todo_model import TodoModel


class TodoPSQLRepository(TodoRepository):
  def __init__(self, session: AsyncSession):
    self.session = session

  async def create_todo(self, todo: Todo) -> Todo:
    db_todo = TodoModel.from_entity(todo)
    self.session.add(db_todo)
    await self.session.flush()
    return db_todo.to_entity()

  async def get_all_todos(self) -> list[Todo]:
    query = select(TodoModel)
    result = await self.session.execute(query)
    todos = result.scalars().all()
    return [todo.to_entity() for todo in todos]

  async def get_all_todos_by_user_id(self, user_id: UUID) -> list[Todo]:
    query = select(TodoModel).where(TodoModel.user_id == user_id)
    result = await self.session.execute(query)
    todos = result.scalars().all()
    return [todo.to_entity() for todo in todos]

  async def get_todo_by_id(self, todo_id: UUID) -> Todo | None:
    result = await self.session.get(TodoModel, todo_id)
    if result is None:
      return None
    return result.to_entity()

  async def update_todo(self, todo: Todo) -> Todo:
    db_todo = TodoModel.from_entity(todo)
    await self.session.merge(db_todo)
    await self.session.flush()
    return db_todo.to_entity()

  async def delete_todo(self, todo_id: UUID) -> None:
    db_todo = await self.session.get(TodoModel, todo_id)
    if db_todo:
      await self.session.delete(db_todo)
      await self.session.flush()
