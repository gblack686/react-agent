"""
Test script for the ReAct agent with MCP integration.

This script tests the agent's ability to use MCP tools
by passing a query that requires accessing external data.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the agent functions
from src.react_agent.mcp_integration import create_mcp_agent
from src.react_agent.graph import graph

async def test_agent_with_mcp():
    """Test the agent's ability to use MCP tools."""
    
    print("Testing agent with MCP tools...")
    
    # Define a test query
    query = "What tables are available in the Supabase database? After listing them, give me a sample record from the users table."
    
    # Run the query through the agent
    try:
        # First try using the graph
        print("\nAttempting to use LangGraph...")
        async with graph() as g:
            result = await g.ainvoke({"messages": [{"role": "user", "content": query}]})
            print("\nLangGraph Response:")
            for message in result["messages"]:
                if message["role"] == "assistant":
                    print(f"Assistant: {message['content']}")
                elif message["role"] == "tool":
                    print(f"Tool ({message.get('name', 'unknown')}): {message['content']}")
    except Exception as e:
        print(f"Error with LangGraph: {e}")
        
        # Fall back to direct agent if graph fails
        print("\nFalling back to direct agent...")
        async with create_mcp_agent() as agent:
            result = await agent.ainvoke({"messages": [{"role": "user", "content": query}]})
            print("\nDirect Agent Response:")
            for message in result["messages"]:
                if message["role"] == "assistant":
                    print(f"Assistant: {message['content']}")
                elif message["role"] == "tool":
                    print(f"Tool ({message.get('name', 'unknown')}): {message['content']}")
    
    print("\nTest completed.")

if __name__ == "__main__":
    asyncio.run(test_agent_with_mcp()) 