# LAS Core Engine Architecture (Based on AgenticSeek)

## Overview
The core engine is built on **Python FastAPI** and follows a modular structure. It initializes a central `Interaction` object that manages state, agents, and the LLM provider.

## Directory Structure
```
core/
├── api.py                 # Main entry point, FastAPI app, API endpoints
├── config.ini             # Configuration file (LLM, Browser, etc.)
├── sources/
│   ├── llm_provider.py    # LLM Provider logic (Ollama, OpenAI, etc.)
│   ├── interaction.py     # Main state manager & conversation loop
│   ├── router.py          # Intent classification & routing logic
│   ├── browser.py         # Selenium/Playwright browser automation
│   ├── agents/            # Agent implementations (Casual, Coder, Planner)
│   ├── tools/             # Tool implementations
│   ├── memory.py          # Session-based memory management
│   └── schemas.py         # Pydantic models for API requests/responses
└── frontend/              # React Frontend
```

## Key Components

### 1. API Layer (`api.py`)
- **Framework**: FastAPI
- **Endpoints**:
    - `POST /query`: Main entry point for user queries.
    - `GET /stop`: Stops the current agent execution.
    - `GET /latest_answer`: Polling endpoint for streaming responses.
    - `GET /health`: Health check.
- **Initialization**: Calls `initialize_system()` to setup Provider, Browser, and Agents.

### 2. LLM Provider (`sources/llm_provider.py`)
- **Class**: `Provider`
- **Role**: Abstracts interactions with different LLM backends.
- **Supported**: Ollama (local), OpenAI, Azure, etc.
- **Configuration**: Defined in `config.ini`.

### 3. Interaction Manager (`sources/interaction.py`)
- **Class**: `Interaction`
- **Role**: Central controller.
    - Manages the active `current_agent`.
    - Handles the "Think" loop (`think()`).
    - Manages TTS/STT if enabled.

### 4. Agents (`sources/agents/`)
- **Base Class**: Likely defined in `sources/agents/base.py` (implied).
- **Types**:
    - `CasualAgent`: Chat & personality.
    - `CoderAgent`: Writes and executes code.
    - `PlannerAgent`: Breaks down complex tasks.
    - `BrowserAgent`: Navigates the web.

### 5. Browser (`sources/browser.py`)
- **Engine**: Selenium with `undetected_chromedriver`.
- **Role**: Performs web scraping, searching, and interaction.

## Data Flow
1.  **User Request**: `POST /query` -> `api.py`
2.  **Processing**: `api.py` calls `interaction.think(query)`
3.  **Routing**: `Interaction` (or `Router`) determines the best Agent.
4.  **Execution**: Selected Agent executes tools/logic using `Provider`.
5.  **Response**: Result is stored in `interaction.last_answer` and returned via API.

## Integration Points for Hybrid Build

- **Vector DB**: Will be integrated into `sources/memory.py` or a new `services/rag_service.py`.
- **LangGraph**: Will replace the current `Interaction` loop and `Router` logic.
- **Tools**: `sources/tools/` will be expanded with AGiXT's extension manager.
