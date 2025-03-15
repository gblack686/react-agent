# Model Context Protocol (MCP) Integration

This project has been enhanced with Model Context Protocol (MCP) integration, allowing the LangGraph React agent to access various external services through standardized interfaces.

## What is MCP?

Model Context Protocol (MCP) is a standard for accessing various external services (like databases, APIs, etc.) through a unified interface. It allows AI agents to interact with external systems without needing to implement custom integrations for each service.

## Supported MCP Services

The current implementation supports the following MCP services:

- **Supabase**: Database operations
- **Notion**: Document and database operations
- **YouTube**: Transcript extraction

## How to Use MCP Tools

The MCP tools are automatically integrated with the ReAct agent and available through the agent's tool selection mechanism. The agent can choose to use these tools when appropriate for solving user queries.

## Docker Setup

This project includes Docker support with a complete setup for both the LangGraph agent and MCP services:

1. **LangGraph Agent**: The main agent that handles user queries
2. **Jina AI MCP Server**: Provides MCP capabilities to the agent
3. **LangGraph Studio**: UI for visualizing and interacting with the agent

### Running with Docker

To start the entire setup with Docker:

```bash
# Copy the example environment file and configure it
cp .env.example .env

# Edit the .env file with your API keys
nano .env

# Start the Docker services
docker-compose up -d
```

Access the LangGraph Studio UI at http://localhost:3000

## Environment Variables

The following environment variables are used for MCP configuration:

- `MCP_SERVER_URL`: URL of the MCP server (default: http://jina-mcp:8080)
- `JINA_MCP_API_KEY`: API key for the Jina AI MCP server
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase API key
- `NOTION_TOKEN`: Notion API token

## Adding New MCP Tools

To add new MCP tools:

1. Update the `src/react_agent/mcp_integration.py` file with new tool functions
2. Add the new tools to the `MCP_TOOLS` list in the same file

## Troubleshooting

- **Connection Issues**: Ensure the MCP server is running and accessible from the agent container
- **Authentication Errors**: Verify the API keys in your .env file
- **Missing Capabilities**: Check if the required MCP service is installed and configured 