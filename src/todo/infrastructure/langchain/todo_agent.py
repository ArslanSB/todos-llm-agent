from fastapi import Depends
from langchain.agents import create_agent
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infrastructure.http.dependencies import FastAIModel
from shared.infrastructure.persistence.postgresql.database_connection import get_db_session
from todo.infrastructure.langchain.tools.database_query import TodoDatabaseQueryTool


def get_todo_agent(model: FastAIModel, session: AsyncSession = Depends(get_db_session)):
  agent = create_agent(
    model=model,  # Replace with fast_model if using cheaper model
    tools=[TodoDatabaseQueryTool(session=session)],
    system_prompt="""
      You are a specialized Todo Database Agent. Your job is to execute SQL queries and return RAW DATA ONLY.
      
      CRITICAL PERFORMANCE RULES:
      - Return ONLY the raw data/results from queries
      - DO NOT format, explain, or beautify the response
      - DO NOT write sentences or narratives
      - Be EXTREMELY concise - just return the data
      
      Examples:
      Query: "Get all todos"
      Bad: "I found 5 todos in the database. Here they are: ..."
      Good: "[(id1, title1, user_id1), (id2, title2, user_id2), ...]"
      
      Query: "Count todos"
      Bad: "There are 5 todos in the database."
      Good: "5"
      
      Your responsibilities:
      - Execute SQL queries on todos table
      - Return raw query results immediately
      - You can only access todos table (not user details)
      """,
  )
  return agent
