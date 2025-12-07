from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  """Application configuration settings."""

  use_ollama: bool = Field(False, description="Whether to use Ollama as the language model backend.", init=False)

  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
  """Get cached application settings."""
  return Settings()
