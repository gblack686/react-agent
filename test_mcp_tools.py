"""
Test script for the MCP tools.

This script tests the MCP tools directly without using the LLM.
"""

import asyncio
import json
from src.react_agent.mcp_integration import list_tables, read_records, get_transcript

async def test_mcp_tools():
    """Test the MCP tools directly."""
    
    print("Testing MCP tools directly...")
    
    # Test list_tables
    print("\n1. Testing list_tables")
    try:
        result = await list_tables()
        print(f"Result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test read_records
    print("\n2. Testing read_records")
    try:
        result = await read_records("users")
        print(f"Result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test get_transcript
    print("\n3. Testing get_transcript")
    try:
        result = await get_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print(f"Result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTest completed.")

if __name__ == "__main__":
    asyncio.run(test_mcp_tools()) 