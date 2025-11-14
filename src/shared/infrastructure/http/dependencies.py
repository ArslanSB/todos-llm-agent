import os
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request
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


UserId = Annotated[UUID, Depends(get_current_user_id)]
