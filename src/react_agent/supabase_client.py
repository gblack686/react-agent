"""Supabase client for direct database access.

This module provides direct access to Supabase without requiring the MCP server.
"""

import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Get Supabase credentials from environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://unickqnwfheaczccvgbw.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVuaWNrcW53ZmhlYWN6Y2N2Z2J3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMzk1MTYxMCwiZXhwIjoyMDQ5NTI3NjEwfQ.fF1rHLTbrfngF9I9DqKmvc2ab-Ms7czmI38j9o0g0kY")


def get_supabase_client() -> Client:
    """Get a Supabase client.
    
    Returns:
        A Supabase client instance.
    """
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        raise


async def list_tables() -> Dict[str, List[str]]:
    """List all tables in the Supabase database.
    
    Returns:
        A dictionary containing the list of tables.
    """
    try:
        # This is a simplified implementation
        # In a real implementation, you'd use the Supabase API to get the table list
        # This is just a placeholder that returns some common table names
        return {"tables": ["users", "products", "orders"]}
    except Exception as e:
        print(f"Error listing tables: {e}")
        return {"tables": [], "error": str(e)}


async def read_records(table: str, filter_params: Optional[Dict[str, Any]] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Read records from a Supabase table.
    
    Args:
        table: The name of the table to read from
        filter_params: Optional filter conditions
        
    Returns:
        A dictionary containing the list of records.
    """
    try:
        supabase = get_supabase_client()
        query = supabase.table(table).select("*")
        
        # Apply filters if provided
        if filter_params:
            for key, value in filter_params.items():
                if isinstance(value, dict) and "eq" in value:
                    query = query.eq(key, value["eq"])
                elif isinstance(value, dict) and "neq" in value:
                    query = query.neq(key, value["neq"])
                elif isinstance(value, dict) and "gt" in value:
                    query = query.gt(key, value["gt"])
                elif isinstance(value, dict) and "lt" in value:
                    query = query.lt(key, value["lt"])
                elif isinstance(value, dict) and "gte" in value:
                    query = query.gte(key, value["gte"])
                elif isinstance(value, dict) and "lte" in value:
                    query = query.lte(key, value["lte"])
                elif isinstance(value, dict) and "like" in value:
                    query = query.like(key, value["like"])
                elif isinstance(value, dict) and "ilike" in value:
                    query = query.ilike(key, value["ilike"])
                else:
                    query = query.eq(key, value)
        
        response = query.execute()
        return {"data": response.data}
    except Exception as e:
        print(f"Error reading records from table {table}: {e}")
        return {"data": [], "error": str(e)}


async def create_record(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new record in a Supabase table.
    
    Args:
        table: The name of the table to create the record in
        data: The record data
        
    Returns:
        A dictionary containing the created record.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table(table).insert(data).execute()
        return {"data": response.data}
    except Exception as e:
        print(f"Error creating record in table {table}: {e}")
        return {"data": [], "error": str(e)}


async def update_record(table: str, data: Dict[str, Any], filter_params: Dict[str, Any]) -> Dict[str, Any]:
    """Update a record in a Supabase table.
    
    Args:
        table: The name of the table to update the record in
        data: The updated record data
        filter_params: Filter conditions to identify the record to update
        
    Returns:
        A dictionary containing the updated record.
    """
    try:
        supabase = get_supabase_client()
        query = supabase.table(table).update(data)
        
        # Apply filters to identify the record to update
        for key, value in filter_params.items():
            if isinstance(value, dict) and "eq" in value:
                query = query.eq(key, value["eq"])
            else:
                query = query.eq(key, value)
        
        response = query.execute()
        return {"data": response.data}
    except Exception as e:
        print(f"Error updating record in table {table}: {e}")
        return {"data": [], "error": str(e)}


async def delete_record(table: str, filter_params: Dict[str, Any]) -> Dict[str, Any]:
    """Delete a record from a Supabase table.
    
    Args:
        table: The name of the table to delete the record from
        filter_params: Filter conditions to identify the record to delete
        
    Returns:
        A dictionary containing the deleted record.
    """
    try:
        supabase = get_supabase_client()
        query = supabase.table(table).delete()
        
        # Apply filters to identify the record to delete
        for key, value in filter_params.items():
            if isinstance(value, dict) and "eq" in value:
                query = query.eq(key, value["eq"])
            else:
                query = query.eq(key, value)
        
        response = query.execute()
        return {"data": response.data}
    except Exception as e:
        print(f"Error deleting record from table {table}: {e}")
        return {"data": [], "error": str(e)} 