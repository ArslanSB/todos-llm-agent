from typing import Type

from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool, ToolException
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel, Field


class TodoSubAgentToolInput(BaseModel):
  """Input for [TodoSubAgentToolInput]"""

  query: str = Field(description=("Plain text query to execute on the todo's sub-agent sent from the main agent."))


class TodoSubAgentTool(BaseTool):
  name: str = "todo_sub_agent"
  description: str = """
    Use this tool to interact with the Todo database sub-agent.
    
    This sub-agent is responsible for:
    - Querying todo items from the database
    - Counting todos
    - Filtering todos by status (completed/incomplete)
    - Finding todos by user_id
    - Getting todo details (title, description, created_at, completed_at, etc.)
    
    Important: This tool returns todo information including user_ids, but does NOT provide user details.
    To get user information (like names, emails), you must use the user_sub_agent separately.
    
    Input: A natural language query about todo items.
    Output: Todo information from the database.
    """  # noqa: E501

  args_schema: Type[BaseModel] = TodoSubAgentToolInput
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
