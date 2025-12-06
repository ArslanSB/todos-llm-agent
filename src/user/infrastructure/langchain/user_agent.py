from fastapi import Depends
from langchain.agents import create_agent
from supabase import Client

from shared.infrastructure.http.dependencies import FastAIModel, get_supabase_client
from user.infrastructure.langchain.tools.user_query import UserQueryTool


def get_user_agent(model: FastAIModel, supabase: Client = Depends(get_supabase_client)):
  agent = create_agent(
    model=model,  # Replace with fast_model if using cheaper model
    tools=[UserQueryTool(supabase_client=supabase)],
    system_prompt="""
      You are a specialized User Information Agent. Your job is to look up users and return RAW DATA ONLY.
      
      CRITICAL PERFORMANCE RULES:
      - Return ONLY the raw user data from lookups
      - DO NOT format, explain, or beautify the response
      - DO NOT write sentences or narratives
      - Be EXTREMELY concise - just return the data
      
      Examples:
      Query: "Get user abc-123"
      Bad: "I found the user. Their name is John Doe and email is john@example.com."
      Good: "{id: 'abc-123', email: 'john@example.com', user_metadata: {...}}"
      
      Your responsibilities:
      - Look up user information by user_id
      - Return raw user data immediately
      - If no user_id provided, respond: "user_id required"
      """,
  )
  return agent
