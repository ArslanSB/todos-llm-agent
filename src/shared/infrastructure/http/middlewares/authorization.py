from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from supabase import Client

from shared.infrastructure.http.dependencies import get_supabase_client


class SupabaseAuthorizationScheme(OAuth2PasswordBearer):
  def __init__(
    self, tokenUrl: str, scheme_name: str | None = None, scopes: dict[str, str] | None = None, auto_error: bool = True
  ) -> None:
    super().__init__(tokenUrl=tokenUrl, scheme_name=scheme_name, scopes=scopes, auto_error=auto_error)
    # routes to exclude from authorization
    self.excluded_paths = ["/health", "/docs", "/openapi.json", "/token"]

  async def __call__(self, request: Request, supabase: Client = Depends(get_supabase_client)) -> None:
    # Skip authorization for excluded paths
    if request.url.path in self.excluded_paths:
      return

    auth_header = request.headers.get("Authorization")
    if not auth_header:
      raise HTTPException(status_code=401, detail="Authorization header missing")

    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    user_response = supabase.auth.get_user(token)

    if not user_response or not user_response.user:
      raise HTTPException(status_code=401, detail="Invalid or expired token")

    request.state.user = user_response.user
