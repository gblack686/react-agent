"""MCP tools for the LangGraph agent.

This module provides tool functions that can be used by the LangGraph agent
to interact with various MCP services.
"""

import os
from typing import Any, Dict, List, Optional, cast

from langchain_core.tools import BaseTool, Tool
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from typing_extensions import Annotated

from mcp.connectors import SupabaseMCP, NotionMCP


# Supabase MCP Tools

async def mcp_supabase_list_tables(
    *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Dict[str, List[str]]:
    """List all tables in the Supabase database.

    Returns:
        A dictionary containing the list of tables.
    """
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_KEY", "")
    
    connector = SupabaseMCP(supabase_url, supabase_key)
    result = await connector.execute("list_tables", {})
    return cast(Dict[str, List[str]], result)


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
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_KEY", "")
    
    connector = SupabaseMCP(supabase_url, supabase_key)
    parameters = {"table": table}
    if filter:
        parameters["filter"] = filter
    
    result = await connector.execute("read_records", parameters)
    return cast(Dict[str, List[Dict[str, Any]]], result)


# Notion MCP Tools

async def mcp_notion_get_database_info(
    *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Dict[str, Any]:
    """Get information about the configured Notion database.

    Returns:
        A dictionary containing database information.
    """
    notion_token = os.environ.get("NOTION_TOKEN", "")
    
    connector = NotionMCP(notion_token)
    result = await connector.execute("get_database_info", {})
    return cast(Dict[str, Any], result)


# List of all MCP tools available to the agent
MCP_TOOLS = [
    mcp_supabase_list_tables,
    mcp_supabase_read_records,
    mcp_notion_get_database_info,
    # Add more tools as needed
] 