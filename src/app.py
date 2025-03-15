"""FastAPI app for serving the ReAct agent."""

import os
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

# Add a health check endpoint
@app.get("/health")
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "langgraph_available": str(has_langgraph)}

# Add a root endpoint
@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint."""
    return {
        "message": "Welcome to the LangGraph ReAct agent with MCP integration",
        "langgraph_available": has_langgraph,
        "endpoints": {
            "agent": "/agent" if has_langgraph else "Not available - LangGraph not installed",
            "health": "/health",
            "mcp": "/mcp/{service}",
        }
    }

# Mock MCP API for testing
@app.post("/mcp/{service}")
async def mock_mcp(service: str, data: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """Mock MCP API endpoint.
    
    This endpoint simulates MCP functionality for testing purposes.
    
    Args:
        service: The service to use (e.g., "supabase", "notion")
        data: The request data containing action and parameters
        
    Returns:
        A simulated response from the service
    """
    action = data.get("action", "")
    parameters = data.get("parameters", {})
    
    print(f"MCP request: service={service}, action={action}, parameters={parameters}")
    
    # Simulate Supabase responses
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