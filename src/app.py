"""FastAPI app for serving the ReAct agent."""
"""March 14 2025 Lets make a change"""

import os
import json
import httpx
from typing import Dict, List, Any, Union

from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the FastAPI app
app = FastAPI(
    title="LangGraph ReAct Agent",
    version="0.1.0",
    description="A ReAct agent built with LangGraph that can access external services via MCP",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP server configuration
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:8080")

try:
    # Try importing LangGraph specific modules
    from langgraph.serde import register_builtins
    from react_agent.graph import graph
    
    # Register the builtins for serialization
    register_builtins()
    
    # Add routes for the agent
    add_routes(
        app,
        graph,
        path="/agent",
    )
    
    has_langgraph = True
except ImportError:
    has_langgraph = False
    print("WARNING: LangGraph modules could not be imported. Some functionality will be limited.")

# Try to import Supabase client for direct access
try:
    import src.react_agent.supabase_client as supabase_client
    has_supabase_client = True
except ImportError:
    has_supabase_client = False
    print("WARNING: Supabase client could not be imported. Will use MCP server if available.")

# Add a health check endpoint
@app.get("/health")
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "ok", 
        "langgraph_available": str(has_langgraph),
        "supabase_client_available": str(has_supabase_client)
    }

# Add a root endpoint
@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint."""
    return {
        "message": "Welcome to the LangGraph ReAct agent with MCP integration",
        "langgraph_available": has_langgraph,
        "supabase_client_available": has_supabase_client,
        "endpoints": {
            "agent": "/agent" if has_langgraph else "Not available - LangGraph not installed",
            "health": "/health",
            "mcp": "/mcp/{service}",
        }
    }

# Check if MCP server is available
async def is_mcp_server_available() -> bool:
    """Check if the MCP server is available.
    
    Returns:
        bool: True if the MCP server is available, False otherwise
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MCP_SERVER_URL}/health", timeout=2.0)
            return response.status_code == 200
    except Exception as e:
        print(f"Error checking MCP server: {e}")
        return False

# MCP API endpoint
@app.post("/mcp/{service}")
async def handle_mcp(service: str, data: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """MCP API endpoint.
    
    This endpoint either forwards requests to the MCP server or uses the local Supabase client.
    
    Args:
        service: The service to use (e.g., "supabase", "notion")
        data: The request data containing action and parameters
        
    Returns:
        A response from the service
    """
    action = data.get("action", "")
    parameters = data.get("parameters", {})
    
    print(f"MCP request: service={service}, action={action}, parameters={parameters}")
    
    # Try to use real MCP server first
    mcp_available = await is_mcp_server_available()
    
    if mcp_available:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{MCP_SERVER_URL}/{service}",
                    json=data,
                    timeout=10.0
                )
                return response.json()
        except Exception as e:
            print(f"Error forwarding to MCP server: {e}")
            # Fall back to local implementation
    
    # Use local Supabase client if available
    if service == "supabase" and has_supabase_client:
        try:
            if action == "list_tables":
                return await supabase_client.list_tables()
            elif action == "read_records":
                table = parameters.get("table", "")
                filter_params = parameters.get("filter", {})
                return await supabase_client.read_records(table, filter_params)
            elif action == "create_record":
                table = parameters.get("table", "")
                record_data = parameters.get("data", {})
                return await supabase_client.create_record(table, record_data)
            elif action == "update_record":
                table = parameters.get("table", "")
                record_data = parameters.get("data", {})
                filter_params = parameters.get("filter", {})
                return await supabase_client.update_record(table, record_data, filter_params)
            elif action == "delete_record":
                table = parameters.get("table", "")
                filter_params = parameters.get("filter", {})
                return await supabase_client.delete_record(table, filter_params)
        except Exception as e:
            print(f"Error using Supabase client: {e}")
            # Fall back to mock responses
    
    # Fallback mock responses
    if service == "supabase":
        if action == "list_tables":
            return {"tables": ["users", "products", "orders"]}
        elif action == "read_records":
            table = parameters.get("table", "")
            return {"data": [{"id": 1, "name": "Sample record from " + table}]}
    
    # Simulate Notion responses
    elif service == "notion":
        if action == "get_database_info":
            return {"database": {"id": "sample-id", "title": "Sample Database"}}
    
    # Simulate YouTube responses
    elif service == "youtube":
        if action == "get_transcript":
            url = parameters.get("url", "")
            return {"transcript": f"Mock transcript for {url}", "language": parameters.get("lang", "en")}
    
    # Default response for unknown services or actions
    return {
        "status": "success", 
        "message": f"Mock response for {service}/{action}",
        "parameters": parameters
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 