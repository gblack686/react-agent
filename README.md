# LangGraph ReAct Agent with MCP Integration
<!-- Updated deployment configuration -->

This project demonstrates how to build a ReAct agent using LangGraph that can access external services via the Model Context Protocol (MCP).

## Overview

The project consists of two main components:

1. **Custom MCP Server**: A Node.js Express server that provides MCP-compatible endpoints for Supabase and YouTube services.
2. **LangGraph ReAct Agent**: A Python-based agent that uses the MCP server to access external services.

## Project Structure

```
.
├── mcp-server/              # Custom MCP server implementation
│   ├── index.js             # MCP server code
│   ├── package.json         # Node.js dependencies
│   └── .env                 # Environment variables for the MCP server
├── src/                     # Source code for the ReAct agent
│   ├── app.py               # FastAPI app for serving the agent
│   └── react_agent/         # ReAct agent implementation
│       ├── graph.py         # LangGraph definition
│       ├── mcp_integration.py # MCP integration code
│       └── supabase_client.py # Direct Supabase client (fallback)
├── test_mcp_tools.py        # Test script for MCP tools
├── test_agent.py            # Test script for the agent
└── README.md                # This file
```

## Setup

### Prerequisites

- Python 3.9+
- Node.js 16+
- Supabase account (optional for real database access)

### Installation

1. Clone the repository:
```
git clone <repository-url>
cd react-agent
```

2. Install Python dependencies:
```
pip install -r requirements.txt
```

3. Install Node.js dependencies for the MCP server:
```
cd mcp-server
npm install
```

4. Create a `.env` file in the root directory with your API keys:
```
# LLM configuration
ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-5-sonnet-20240620

# Database configuration
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# MCP Server
MCP_SERVER_URL=http://localhost:8080
```

5. Create a `.env` file in the `mcp-server` directory with your Supabase credentials:
```
# Supabase Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# Server Configuration
PORT=8080
```

## Running the Application

1. Start the MCP server:
```
cd mcp-server
node index.js
```

2. Start the FastAPI server:
```
python -m uvicorn src.app:app --reload
```

3. Access the API at http://localhost:8000

## Testing

1. Test the MCP tools directly:
```
python test_mcp_tools.py
```

2. Test the agent with MCP integration:
```
python test_agent.py
```

## MCP Integration

This project demonstrates two approaches to MCP integration:

1. **Direct HTTP Calls**: The `mcp_integration.py` module provides functions that make direct HTTP calls to the MCP server.

2. **LangChain MCP Adapters**: The project can be extended to use the `langchain-mcp-adapters` library for a more standardized approach.

## Available MCP Services

### Supabase

- `list_tables`: List all tables in the Supabase database
- `read_records`: Read records from a Supabase table
- `create_record`: Create a new record in a Supabase table
- `update_record`: Update a record in a Supabase table
- `delete_record`: Delete a record from a Supabase table

### YouTube

- `get_transcript`: Extract transcript from a YouTube video

## License

MIT