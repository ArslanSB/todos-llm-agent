# 🤖 ToDo's LLM Agent

A learning project demonstrating a **multi-agent AI architecture** built with [LangChain](https://www.langchain.com/). This application combines a traditional REST API for ToDo management with an intelligent conversational interface that allows querying the application in natural language.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [License](#license)

## 🎯 Overview

This project showcases a ToDo application with a unique twist: it features an AI-powered chat interface that can answer questions about your todos and user information using natural language. The project implements:

- **Clean Architecture** principles with domain-driven design
- **Multi-Agent System** with specialized sub-agents for different data sources
- **Role-Based Access Control** with admin and regular user permissions (partially!)
- **Supabase Authentication** for secure user management
- **PostgreSQL** for data persistence with async SQLAlchemy

## ✨ Features

### REST API
- ✅ Create, read, update, and delete todos
- ✅ User authentication via Supabase
- ✅ User-specific todo filtering
- ✅ Clean separation of concerns with use cases

### AI Chat Interface
- 🤖 Natural language queries about todos and users
- 🎯 Multi-agent coordination system:
  - **Main Coordinator Agent**: Orchestrates sub-agents and formats responses
  - **Todo Sub-Agent**: Executes SQL queries on the todos database
  - **User Sub-Agent**: Retrieves user information from Supabase
- 🔐 Context-aware permissions (admin vs regular user)
- 💬 Streaming responses for real-time interaction
- 🧠 Persistent conversation memory per thread

### Example Queries
- "How many todos do I have?"
- "Show me all incomplete todos"
- "Who created the most todos?" (admin only)
- "Get user details for user <user_id>"

## 🏗️ Architecture

The application uses a **multi-agent architecture** with LangChain:

```
┌─────────────────────────────────────────────────┐
│          Main Coordinator Agent                 │
│  (Orchestrates, formats, handles permissions)   │
└──────────────┬──────────────────────────────────┘
               │
       ┌───────┴───────┐
       │               │
┌──────▼──────┐  ┌─────▼──────┐
│  Todo Agent │  │ User Agent │
│  (SQL DB)   │  │ (Supabase) │
└─────────────┘  └────────────┘
```

**Agent Responsibilities:**
- **Coordinator**: Manages sub-agents, enforces access control, formats user-friendly responses
- **Todo Agent**: Raw data retrieval from PostgreSQL database
- **User Agent**: User information lookup from Supabase

**Key Design Patterns:**
- Clean Architecture with domain, application, and infrastructure layers
- Dependency Injection for loosely coupled components
- Repository pattern for data access
- Value Objects for domain validation

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance async web framework
- **AI/LLM**: 
  - [LangChain](https://www.langchain.com/) - LLM application framework
  - [OpenAI GPT-4](https://openai.com/) - Language models
  - [LangSmith](https://www.langchain.com/langsmith) - Debugging and tracing (optional)
- **Database**: 
  - [PostgreSQL](https://www.postgresql.org/) - Primary database
  - [SQLAlchemy](https://www.sqlalchemy.org/) - Async ORM
  - [Alembic](https://alembic.sqlalchemy.org/) - Database migrations
- **Authentication**: [Supabase](https://supabase.com/) - Auth and user management
- **Python**: 3.12+
- **Package Manager**: [uv](https://github.com/astral-sh/uv)

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12 or higher**
- **PostgreSQL** (local installation or Docker)
- **uv** package manager (recommended) or pip
- **Supabase Account** (free tier works)
- **OpenAI API Key** with access to GPT-4 (not required if running locally using Ollama)

### Installing uv (Recommended)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 🚀 Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ArslanSB/todos-llm-agent.git
cd todos-llm-agent
```

### 2. Set Up Python Environment

Using **uv** (recommended):
```bash
# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

Using **pip**:
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 3. Set Up Supabase

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Navigate to **Settings** → **API**
4. Copy your **Project URL** and **anon/public API key**
5. Create test users in **Authentication** → **Users**

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database Configuration (PostgreSQL)
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=langchain_db_agent

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_API_KEY=your-supabase-anon-key

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key

# LangSmith Configuration (Optional - for debugging and tracing)
# Sign up at https://smith.langchain.com/
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://<region>.api.smith.langchain.com
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_PROJECT=langchain-db-agent
```

### 5. Set Up PostgreSQL Database

#### Option A: Local PostgreSQL

```bash
# Install PostgreSQL (macOS with Homebrew)
brew install postgresql@15
brew services start postgresql@15

# Create database
createdb langchain_db_agent

# Or using psql
psql postgres
CREATE DATABASE langchain_db_agent;
\q
```

#### Option B: Docker PostgreSQL

```bash
docker run --name postgres-langchain \
  -e POSTGRES_DB=langchain_db_agent \
  -e POSTGRES_USER=your_db_user \
  -e POSTGRES_PASSWORD=your_db_password \
  -p 5432:5432 \
  -d postgres:15
```

## 📊 Database Setup

### Run Migrations

```bash
# Run all migrations to set up database schema
alembic upgrade head
```

### Migration Files

The project includes two migrations:
1. `d5caf946ba43` - Initial setup (creates todos table)
2. `4b00560fceb7` - Adds user_id column to todos

### Create New Migration (if needed)

```bash
# Generate a new migration
alembic revision --autogenerate -m "description of changes"

# Apply the migration
alembic upgrade head
```

## 🏃 Running the Application

### Start the Development Server

```bash
# With uvicorn directly
uvicorn src.main:fast_api --reload --host 0.0.0.0 --port 8000

# Or if you have a start script
python -m uvicorn src.main:fast_api --reload
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Testing the Chat Interface

```bash
# Example using curl (you'll need a valid access token)
curl -X GET "http://localhost:8000/chat?message=How%20many%20todos%20do%20I%20have?&thread_id=550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer YOUR_SUPABASE_TOKEN"
```

## 📚 API Documentation

### Authentication

All endpoints (except `/docs`, `/openapi.json`, `/token`) require authentication via Supabase JWT token.

**Get Token** (for testing):
```bash
POST /token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=your_password
```

### REST Endpoints

#### ToDo Endpoints

- `GET /todos/` - List all todos for authenticated user
- `POST /todos/` - Create a new todo
- `GET /todos/{todo_id}` - Get specific todo
- `PUT /todos/{todo_id}` - Update a todo
- `DELETE /todos/{todo_id}` - Delete a todo

#### Chat Endpoint

- `GET /chat` - Natural language query interface
  - Query params: `message`, `thread_id`
  - Returns: Streaming text response

### Access Control

**Regular User**:
- Can only access their own todos
- Can only query their own user information

**Admin User** (hardcoded for demo):
- User ID: `7fd0b380-4d6e-41a9-b376-33527987467c`
- Can access all todos and user information

## 📁 Project Structure

```
langchain-db-agent/
├── src/
│   ├── main.py                    # FastAPI application entry point
│   ├── shared/                    # Shared infrastructure
│   │   ├── domain/
│   │   └── infrastructure/
│   │       ├── http/
│   │       │   ├── dependencies.py        # DI configuration
│   │       │   └── middlewares/
│   │       │       └── authorization.py   # Supabase auth
│   │       └── persistence/
│   │           └── postgresql/
│   │               ├── database_connection.py
│   │               └── declarative_base.py
│   ├── todo/                      # ToDo module (Clean Architecture)
│   │   ├── application/           # Use cases
│   │   │   ├── create_todo_uc.py
│   │   │   ├── get_todos_uc.py
│   │   │   └── ...
│   │   ├── domain/                # Domain entities
│   │   │   ├── todo.py
│   │   │   ├── todo_repository.py
│   │   │   └── value_objects/
│   │   └── infrastructure/
│   │       ├── http/              # REST API
│   │       │   ├── routes.py
│   │       │   └── schemas/
│   │       ├── langchain/         # AI Agents
│   │       │   ├── todo_agent.py
│   │       │   └── tools/
│   │       │       ├── database_query.py
│   │       │       └── todo_sub_agent.py
│   │       └── persistence/
│   │           └── postgresql/
│   └── user/                      # User module
│       └── infrastructure/
│           └── langchain/
│               ├── user_agent.py
│               └── tools/
├── migrations/                    # Alembic migrations
│   ├── versions/
│   └── env.py
├── pyproject.toml                 # Project dependencies
├── alembic.ini                    # Alembic configuration
└── README.md
```

## 🧪 Code Quality

### Linting and Formatting

The project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Fix auto-fixable issues
ruff check --fix .
```

### Configuration

- **Line length**: 120 characters
- **Indent**: 2 spaces
- **Quote style**: Double quotes
- **Import sorting**: Enabled (isort)

## 🤝 Contributing

This is a learning project, but contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is for educational purposes. Feel free to use it as a learning resource or starting point for your own projects.

## 🙏 Acknowledgments

- Built while learning LangChain and multi-agent systems
- Special thanks to [Eden Marco](https://github.com/emarco177) for his excellent Udemy course on AI Agents, which helped establish the fundamentals
- Inspired by clean architecture principles
- Thanks to the LangChain community for excellent documentation

---

**Happy Learning! 🚀**

For questions or issues, please open an issue on GitHub.
