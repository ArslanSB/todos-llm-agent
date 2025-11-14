from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infrastructure.persistence.postgresql.database_connection import get_db_session
from todo.application.create_todo_uc import CreateTodoUC
from todo.application.delete_todo_uc import DeleteTodoUC
from todo.application.get_todo_uc import GetTodoUC
from todo.application.get_todos_uc import GetTodosUC
from todo.application.update_todo_uc import UpdateTodoUC
from todo.domain.todo_repository import TodoRepository
from todo.infrastructure.persistence.postgresql.todo_psql_repository import TodoPSQLRepository


def get_todo_repository(db: AsyncSession = Depends(get_db_session)) -> TodoRepository:
  return TodoPSQLRepository(session=db)


def get_create_todo_uc(todo_repository: TodoRepository = Depends(get_todo_repository)):
  return CreateTodoUC(todo_repository=todo_repository)


def get_todos_uc(todo_repository: TodoRepository = Depends(get_todo_repository)):
  return GetTodosUC(todo_repository=todo_repository)


def get_todo_uc(todo_repository: TodoRepository = Depends(get_todo_repository)):
  return GetTodoUC(todo_repository=todo_repository)


def get_update_todo_uc(todo_repository: TodoRepository = Depends(get_todo_repository)):
  return UpdateTodoUC(todo_repository=todo_repository)


def get_delete_todo_uc(todo_repository: TodoRepository = Depends(get_todo_repository)):
  return DeleteTodoUC(todo_repository=todo_repository)


CreateTodoUseCase = Annotated[CreateTodoUC, Depends(get_create_todo_uc)]
GetTodosUseCase = Annotated[GetTodosUC, Depends(get_todos_uc)]
GetTodoUseCase = Annotated[GetTodoUC, Depends(get_todo_uc)]
UpdateTodoUseCase = Annotated[UpdateTodoUC, Depends(get_update_todo_uc)]
DeleteTodoUseCase = Annotated[DeleteTodoUC, Depends(get_delete_todo_uc)]
