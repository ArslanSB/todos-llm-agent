from dataclasses import dataclass
from typing import Annotated, AsyncGenerator
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, dynamic_prompt
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph
from starlette.middleware.cors import CORSMiddleware
from supabase import AuthApiError, Client

from shared.infrastructure.http.dependencies import AIModel, UserId, get_supabase_client
from shared.infrastructure.http.middlewares.authorization import SupabaseAuthorizationScheme
from todo.infrastructure.http.routes import routes as todo_router
from todo.infrastructure.langchain.todo_agent import get_todo_agent
from todo.infrastructure.langchain.tools.todo_sub_agent import TodoSubAgentTool
from user.infrastructure.langchain.user_agent import get_user_agent
from user.infrastructure.langchain.user_sub_agent import UserSubAgentTool

supabase_scheme = SupabaseAuthorizationScheme(tokenUrl="token")
checkpoint_saver = InMemorySaver()


fast_api = FastAPI(
  title="LangChain DB Agent",
  description="An API made for testing purposes building LangChain DB Agent",
  version="0.0.1",
  dependencies=[Depends(supabase_scheme)],
)

fast_api.add_middleware(
  CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
fast_api.include_router(todo_router)


@fast_api.exception_handler(Exception)
async def unauthorized_exception_handler(request: Request, exc: Exception):
  if isinstance(exc, HTTPException) and exc.status_code == 401:
    return JSONResponse(status_code=401, content={"detail": str(exc)})
  return JSONResponse(status_code=500, content={"detail": str(exc)})


# NOTE: Helper for documentation
@fast_api.post("/token", tags=["Authentication"], include_in_schema=False)
async def get_token(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()], supabase: Client = Depends(get_supabase_client)
):
  """
  This is a placeholder endpoint for obtaining an authentication token in the documentation.
  In a real application, this is not required since authentication is handled via Supabase & some sort of Frontend.
  """
  try:
    auth_response = supabase.auth.sign_in_with_password({"email": form_data.username, "password": form_data.password})
    if auth_response is None or auth_response.session is None:
      raise HTTPException(status_code=401, detail="Invalid credentials")
  except AuthApiError as e:
    raise HTTPException(status_code=401, detail=str(e))

  return {"access_token": auth_response.session.access_token, "token_type": "bearer"}


@dataclass
class AgentContext:
  user_id: str


@dynamic_prompt
def context_aware_prompt(request: ModelRequest) -> str:
  user_id = request.runtime.context.user_id  #  type: ignore

  if (
    user_id == "7fd0b380-4d6e-41a9-b376-33527987467c"
  ):  # Since we don't have roles in supabase as of now, hardcoding admin user id
    return f"""
    CRITICAL ACCESS CONTROL INFORMATION:
    
    Current User ID: {user_id}
    Access Level: ADMINISTRATOR
    
    This user has FULL ADMIN ACCESS:
    - Can view, modify, and delete ALL todo items in the database (not just their own)
    - Can query information for ANY user in Supabase
    - Has no restrictions on database queries or user lookups
    
    When handling requests:
    - Do NOT filter todos by user_id unless explicitly requested
    - Allow access to all users' information
    - No permission checks needed for this user
    """
  else:
    return f"""
    CRITICAL ACCESS CONTROL INFORMATION:
    
    Current User ID: {user_id}
    Access Level: REGULAR USER (RESTRICTED)
    
    This user has LIMITED ACCESS ONLY:
    - Can ONLY view their OWN todo items (user_id = {user_id})
    - Can ONLY access their OWN user information
    - MUST NOT access other users' todos or information
    
    MANDATORY SECURITY RULES:
    - When querying todos, ALWAYS filter by user_id = '{user_id}'
    - When querying user information, ONLY allow queries for user_id = '{user_id}'
    - REJECT any attempts to access other users' data
    - If asked about other users or their todos, respond: "You don't have permission to access that information"
    """


@fast_api.get("/chat", tags=["Chat"])
async def chat_endpoint(
  message: str,
  thread_id: UUID,
  user_id: UserId,
  model: AIModel,
  todo_agent: CompiledStateGraph = Depends(get_todo_agent),
  user_agent: CompiledStateGraph = Depends(get_user_agent),
):
  """
  An example chat endpoint that uses the GPT chatbot to respond to user messages.
  """
  context = AgentContext(user_id=str(user_id))

  # Create Agent that will manage sub agents
  agent = create_agent(
    model=model,
    tools=[TodoSubAgentTool(agent=todo_agent), UserSubAgentTool(agent=user_agent)],
    context_schema=AgentContext,
    checkpointer=checkpoint_saver,
    middleware=[context_aware_prompt],
    system_prompt="""
      You are a coordinator assistant that manages two specialized sub-agents:
      
      1. **todo_sub_agent**: Handles all todo database queries (counting, listing, filtering todos)
         - Returns RAW todo data including user_ids (not formatted responses)
         - Does NOT provide user details (names, emails)
      
      2. **user_sub_agent**: Handles all user information queries
         - Requires user_id as input
         - Returns RAW user data (not formatted responses)
      
      CRITICAL PERFORMANCE OPTIMIZATION:
      - Sub-agents return RAW DATA ONLY (not formatted text)
      - YOU are responsible for all formatting and presenting to the user
      - Parse the raw data from sub-agents and format it nicely for the user
      
      CRITICAL WORKFLOW RULES:
      - When a question involves BOTH todos AND user information, you MUST call BOTH sub-agents
      - First, call todo_sub_agent to get todo data (which includes user_ids)
      - Then, extract the user_ids from the todo results
      - Finally, call user_sub_agent for EACH unique user_id to get user details
      - Combine the results to provide a complete answer
      
      Examples:
      
      User: "How many todos are there? Who do they belong to?"
      Your workflow:
      1. Call todo_sub_agent: "Get all todos with their user_ids"
      2. Parse the raw data and extract unique user_ids
      3. Call user_sub_agent for each user_id: "Get user details for user_id X"
      4. Parse user data and combine: "There are 5 todos belonging to: Alice (3 todos), Bob (2 todos)"
      
      User: "Who is user abc-123?"
      Your workflow:
      1. Call user_sub_agent: "Get user abc-123"
      2. Parse the raw user data returned
      3. Format nicely: "This is John Doe (john@example.com)"
      
      Remember: 
      - Sub-agents give you raw data, YOU do the formatting
      - ALWAYS use both agents when the question involves users and todos together
      """,
  )

  async def get_response(message: str) -> AsyncGenerator[str, None]:
    async for token, metadata in agent.astream(
      {"messages": [HumanMessage(content=message)]},
      stream_mode="messages",
      context=context,
      config={"configurable": {"thread_id": str(thread_id)}},
    ):
      print(token)
      if metadata["langgraph_node"] == "model" and token.content:
        yield token.content

  return StreamingResponse(get_response(message), media_type="text/event-stream")
