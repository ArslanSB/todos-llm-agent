import os
import uuid
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from supabase import Client, create_client


def get_current_user_id(request: Request) -> UUID:
  """
  Dependency to extract the current user's ID from the request state.
  Assumes that the AuthorizationMiddleware has already populated request.state.user.
  """
  user = getattr(request.state, "user", None)
  if user is None or not hasattr(user, "id"):
    raise ValueError("User not authenticated or user ID not found in request state")

  return UUID(user.id)


def get_supabase_client() -> Client:
  supabase_url = os.getenv("SUPABASE_URL")
  supabase_key = os.getenv("SUPABASE_API_KEY")

  if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL and SUPABASE_API_KEY must be set in environment variables")

  return create_client(supabase_url, supabase_key)


def get_ai_model() -> BaseChatModel:
  # Main agent model - uses more capable model for coordination and formatting
  model = ChatOpenAI(model="gpt-4o", temperature=0)
  return model


def get_fast_ai_model() -> BaseChatModel:
  # Sub-agent model - uses a faster, cheaper model for data retrieval tasks
  model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
  return model


def generate_uuid() -> UUID:
  return uuid.uuid4()


UserId = Annotated[UUID, Depends(get_current_user_id)]
AIModel = Annotated[BaseChatModel, Depends(get_ai_model)]
FastAIModel = Annotated[BaseChatModel, Depends(get_fast_ai_model)]
Uuid = Annotated[UUID, Depends(generate_uuid)]
