from typing import Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from supabase import Client


class UserQueryInput(BaseModel):
  """Input for [UserQueryTool]"""

  user_id: str = Field(description=("ID of the user to query Supabase for."))


class UserQueryTool(BaseTool):
  name: str = "user_supabase_query"
  description: str = """
    A tool for querying users to Supabase.

    Rules:
    1. This tool can only be used by admin users to perform queries to the Supabase.
    """  # noqa: E501

  args_schema: Type[BaseModel] = UserQueryInput

  class Config:
    extra = "allow"

  def __init__(self, supabase_client: Client):
    super().__init__()
    self.supabase_client = supabase_client

  def _run(self, user_id: str) -> str:
    raise NotImplementedError("Synchronous execution is not supported for supabase queries.")

  async def _arun(self, user_id: str) -> dict:
    return self.supabase_client.auth.admin.get_user_by_id(user_id).model_dump()
