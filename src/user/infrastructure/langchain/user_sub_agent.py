from typing import Type

from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool, ToolException
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel, Field


class UserSubAgentToolInput(BaseModel):
  """Input for [UserSubAgentToolInput]"""

  query: str = Field(description=("Plain text query to execute on the user's sub-agent sent from the main agent."))


class UserSubAgentTool(BaseTool):
  name: str = "user_sub_agent"
  description: str = """
    Use this tool to interact with the User information sub-agent.
    
    This sub-agent is responsible for:
    - Getting user details by user_id (name, email, metadata)
    - Looking up user information from Supabase
    - Converting user_ids to human-readable user information
    
    Important: You need to provide a user_id to this tool. If you have user_ids from todos,
    use this tool to get the actual user details.
    
    Input: A natural language query about users, typically including a user_id.
    Output: User information from Supabase.
    """  # noqa: E501

  args_schema: Type[BaseModel] = UserSubAgentToolInput
  handle_tool_error: bool = True

  class Config:
    extra = "allow"

  def __init__(self, agent: CompiledStateGraph):
    super().__init__(agent=agent)
    self.agent = agent

  def _run(self, query: str) -> str:
    # Synchronous execution is not supported for database queries.
    raise NotImplementedError("Synchronous execution is not supported for database queries.")

  async def _arun(self, query: str) -> str:
    try:
      response = await self.agent.ainvoke({"messages": [HumanMessage(content=query)]})
      return response["messages"][-1].content
    except Exception as e:
      raise ToolException(f"Error executing todo sub-agent query: {str(e)}") from e
