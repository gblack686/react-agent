"""MCP integration for the React agent.

This module provides functions to connect the React agent with MCP servers.
"""

import os
import json
import httpx
from typing import Any, Dict, List, Optional, cast

from langchain_core.tools import BaseTool, StructuredTool
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from typing_extensions import Annotated


# MCP server configuration
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://jina-mcp:8080")
MCP_API_KEY = os.environ.get("JINA_MCP_API_KEY", "")


async def _call_mcp_server(endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Any:
    """Make a call to the MCP server.

    Args:
        endpoint: The endpoint to call
        method: The HTTP method to use
        data: The data to send in the request body

    Returns:
        The response from the MCP server
    """
    url = f"{MCP_SERVER_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {MCP_API_KEY}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(url, headers=headers)
        elif method == "POST":
            response = await client.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
            
        response.raise_for_status()
        return response.json()


# Supabase MCP Tools

async def mcp_supabase_list_tables(
    *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Dict[str, List[str]]:
    """List all tables in the Supabase database.

    Returns:
        A dictionary containing the list of tables.
    """
    response = await _call_mcp_server(
        "supabase", 
        method="POST", 
        data={
            "action": "list_tables",
            "parameters": {}
        }
    )
    return cast(Dict[str, List[str]], response)


async def mcp_supabase_read_records(
    table: str,
    filter: Optional[Dict[str, Any]] = None,
    *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Dict[str, List[Dict[str, Any]]]:
    """Read records from a Supabase table.

    Args:
        table: The name of the table to read from
        filter: Optional filter conditions

    Returns:
        A dictionary containing the list of records.
    """
    parameters = {"table": table}
    if filter:
        parameters["filter"] = filter
    
    response = await _call_mcp_server(
        "supabase", 
        method="POST", 
        data={
            "action": "read_records",
            "parameters": parameters
        }
    )
    return cast(Dict[str, List[Dict[str, Any]]], response)


# Notion MCP Tools

async def mcp_notion_get_database_info(
    *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Dict[str, Any]:
    """Get information about the configured Notion database.

    Returns:
        A dictionary containing database information.
    """
    response = await _call_mcp_server(
        "notion", 
        method="POST", 
        data={
            "action": "get_database_info",
            "parameters": {}
        }
    )
    return cast(Dict[str, Any], response)


# YouTube Transcript MCP Tools

async def mcp_youtube_get_transcript(
    url: str,
    lang: str = "en",
    *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Dict[str, Any]:
    """Extract transcript from a YouTube video.

    Args:
        url: YouTube video URL or ID
        lang: Language code for transcript (e.g., 'en', 'es')

    Returns:
        A dictionary containing the transcript.
    """
    response = await _call_mcp_server(
        "youtube", 
        method="POST", 
        data={
            "action": "get_transcript",
            "parameters": {
                "url": url,
                "lang": lang
            }
        }
    )
    return cast(Dict[str, Any], response)


# List of all MCP tools available to the agent
MCP_TOOLS = [
    mcp_supabase_list_tables,
    mcp_supabase_read_records,
    mcp_notion_get_database_info,
    mcp_youtube_get_transcript,
    # Add more tools as needed
] 