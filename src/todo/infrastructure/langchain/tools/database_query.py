from typing import Sequence, Type

from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field
from sqlalchemy import Result, Row, text
from sqlalchemy.ext.asyncio import AsyncSession


class TodoDatabaseQueryInput(BaseModel):
  """Input for [TodoDatabaseQueryTool]"""

  query: str = Field(description=("SQL query to execute on the database."))


class TodoDatabaseQueryTool(BaseTool):
  name: str = "todo_database_query"
  description: str = """
    A tool for querying the todo database.

    Rules:
    1. This tool can only be used to perform read-only operations (SELECT queries) on the database.
    2. This tool must not be used to perform any write operations (INSERT, UPDATE, DELETE, etc.) on the database.
    3. This tool can only run single query at a time.
    4. This tool should only be used to execute safe and authorized read-only SQL queries.
    5. Always ensure that the queries adhere to the database schema provided below.

    ---

    The database has the following schema:
      Table: todos
      Columns:
        - id: UUID, Primary Key
        - title: String, Title of the to-do item
        - description: String, Description of the to-do item
        - user_id: UUID from supabase, ID of the user who owns the to-do item
        - completed: Boolean, Status of the to-do item (completed or not), do not use 0/1 use TRUE/FALSE
        - created_at: DateTime, Timestamp when the to-do item was created
        - updated_at: DateTime, Timestamp when the to-do item was last updated
        - completed_at: DateTime, Timestamp when the to-do item was completed (nullable)
    """  # noqa: E501

  args_schema: Type[BaseModel] = TodoDatabaseQueryInput
  handle_tool_error: bool = True

  class Config:
    extra = "allow"

  def __init__(self, session: AsyncSession):
    super().__init__(session=session)
    self.session = session

  def _run(self, query: str) -> str:
    # Synchronous execution is not supported for database queries.
    raise NotImplementedError("Synchronous execution is not supported for database queries.")

  async def _arun(self, query: str) -> Sequence[Row]:
    result: Result = await self.session.execute(text(query))
    rows = result.fetchall()

    if not rows:
      raise ToolException("The query returned no results.")

    return rows
