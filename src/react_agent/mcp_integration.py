"""
MCP Integration Module

This module integrates the langchain-mcp-adapters library with our custom MCP server
to provide LangChain-compatible tools for the ReAct agent.
"""

import os
import asyncio
import httpx
from typing import List, Dict, Any, Optional, Callable
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Import LangChain and MCP components
from langchain_core.tools import BaseTool, Tool
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# MCP server configuration
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:8080")

# Configure HTTP client for MCP server communication
async def call_mcp_endpoint(service: str, action: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Call an MCP endpoint with the given service, action, and parameters.
    
    Args:
        service: The MCP service to call (e.g., 'supabase', 'youtube')
        action: The action to perform on the service
        parameters: The parameters for the action
        
    Returns:
        The response from the MCP server
    """
    if parameters is None:
        parameters = {}
        
    payload = {
        "action": action,
        "parameters": parameters
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MCP_SERVER_URL}/{service}",
                json=payload,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"Error calling MCP endpoint {service}/{action}: {e}")
        return {"error": str(e)}

# Create tool functions for Supabase operations
async def list_tables(kwargs: Dict[str, Any] = None) -> Dict[str, List[str]]:
    """List all tables in the Supabase database."""
    result = await call_mcp_endpoint("supabase", "list_tables")
    return result

async def read_records(table: str, filter: Dict[str, Any] = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Read records from a Supabase table.
    
    Args:
        table: The table name to read from
        filter: Optional filter conditions
    """
    parameters = {"table": table}
    if filter:
        parameters["filter"] = filter
        
    result = await call_mcp_endpoint("supabase", "read_records", parameters)
    return result

async def create_record(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new record in a Supabase table.
    
    Args:
        table: The table name to create the record in
        data: The record data
    """
    parameters = {
        "table": table,
        "data": data
    }
    
    result = await call_mcp_endpoint("supabase", "create_record", parameters)
    return result

async def update_record(table: str, data: Dict[str, Any], filter: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a record in a Supabase table.
    
    Args:
        table: The table name to update
        data: The updated data
        filter: Filter conditions to identify the record(s) to update
    """
    parameters = {
        "table": table,
        "data": data,
        "filter": filter
    }
    
    result = await call_mcp_endpoint("supabase", "update_record", parameters)
    return result

async def delete_record(table: str, filter: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete a record from a Supabase table.
    
    Args:
        table: The table name to delete from
        filter: Filter conditions to identify the record(s) to delete
    """
    parameters = {
        "table": table,
        "filter": filter
    }
    
    result = await call_mcp_endpoint("supabase", "delete_record", parameters)
    return result

# Create tool functions for YouTube operations
async def get_transcript(url: str, lang: str = "en") -> Dict[str, Any]:
    """
    Extract transcript from a YouTube video.
    
    Args:
        url: YouTube video URL or ID
        lang: Language code for transcript (e.g., 'en', 'es')
    """
    parameters = {
        "url": url,
        "lang": lang
    }
    
    result = await call_mcp_endpoint("youtube", "get_transcript", parameters)
    return result

def get_mcp_tools() -> List[BaseTool]:
    """
    Get all available MCP tools.
    
    Returns:
        A list of LangChain tools for the MCP services.
    """
    tools = [
        Tool(
            name="list_tables",
            description="List all tables in the Supabase database",
            func=list_tables,
            coroutine=list_tables
        ),
        Tool(
            name="read_records",
            description="Read records from a Supabase table. Requires table name and optional filter conditions.",
            func=read_records,
            coroutine=read_records
        ),
        Tool(
            name="create_record",
            description="Create a new record in a Supabase table. Requires table name and record data.",
            func=create_record,
            coroutine=create_record
        ),
        Tool(
            name="update_record",
            description="Update a record in a Supabase table. Requires table name, updated data, and filter conditions.",
            func=update_record,
            coroutine=update_record
        ),
        Tool(
            name="delete_record",
            description="Delete a record from a Supabase table. Requires table name and filter conditions.",
            func=delete_record,
            coroutine=delete_record
        ),
        Tool(
            name="get_youtube_transcript",
            description="Extract transcript from a YouTube video. Requires video URL and optional language code.",
            func=get_transcript,
            coroutine=get_transcript
        )
    ]
    
    return tools

@asynccontextmanager
async def create_mcp_agent():
    """
    Create a ReAct agent that can use MCP tools.
    
    Returns:
        A LangGraph agent configured with MCP tools.
    """
    # Initialize the LLM
    llm = ChatAnthropic(
        model=os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620"),
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
        temperature=0
    )
    
    # Get all MCP tools
    tools = get_mcp_tools()
    
    # Create the agent
    agent = create_react_agent(llm, tools)
    
    yield agent 