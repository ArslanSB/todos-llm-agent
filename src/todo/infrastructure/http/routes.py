from uuid import UUID

from fastapi import APIRouter

from shared.infrastructure.http.dependencies import UserId
from todo.infrastructure.http.dependencies import (
  CreateTodoUseCase,
  DeleteTodoUseCase,
  GetTodosUseCase,
  GetTodoUseCase,
  UpdateTodoUseCase,
)
from todo.infrastructure.http.schemas.todo import Todo as TodoSchema

routes = APIRouter(prefix="/todos", tags=["ToDo"])


@routes.get("/", response_model=list[TodoSchema])
async def read_todos(use_case: GetTodosUseCase, user_id: UserId):
  todos = await use_case.execute(user_id=user_id)
  return [TodoSchema.from_domain(todo) for todo in todos]


@routes.post("/", response_model=TodoSchema)
async def create_todo(title: str, description: str, use_case: CreateTodoUseCase, user_id: UserId):
  todo = await use_case.execute(title=title, description=description, user_id=user_id)
  return TodoSchema.from_domain(todo)


@routes.get("/{todo_id}", response_model=TodoSchema)
async def read_todo(todo_id: UUID, user_id: UserId, use_case: GetTodoUseCase):
  todo = await use_case.execute(todo_id=todo_id, user_id=user_id)
  return TodoSchema.from_domain(todo)


@routes.put("/{todo_id}", response_model=TodoSchema)
async def update_todo(
  todo_id: UUID,
  user_id: UserId,
  use_case: UpdateTodoUseCase,
  title: str | None = None,
  description: str | None = None,
  completed: bool | None = None,
):
  todo = await use_case.execute(
    todo_id=todo_id, title=title, description=description, completed=completed, user_id=user_id
  )
  return TodoSchema.from_domain(todo)


@routes.delete("/{todo_id}")
async def delete_todo(todo_id: UUID, user_id: UserId, use_case: DeleteTodoUseCase):
  return await use_case.execute(todo_id=todo_id, user_id=user_id)
