from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from supabase import AuthApiError, Client

from shared.infrastructure.http.dependencies import get_supabase_client
from shared.infrastructure.http.middlewares.authorization import SupabaseAuthorizationScheme
from todo.infrastructure.http.routes import routes as todo_router

supabase_scheme = SupabaseAuthorizationScheme(tokenUrl="token")

fast_api = FastAPI(
  title="LangChain DB Agent",
  description="An API made for testing purposes building LangChain DB Agent",
  version="0.0.1",
  dependencies=[Depends(supabase_scheme)],
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
