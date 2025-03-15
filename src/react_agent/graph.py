"""
LangGraph ReAct agent definition.

This module defines the ReAct agent graph using LangGraph.
"""

import os
from contextlib import asynccontextmanager
from typing import Dict, List, Tuple, Any, Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv

# Import our MCP integration
from react_agent.mcp_integration import get_mcp_tools, create_mcp_agent

# Load environment variables
load_dotenv()

# Define the agent state
class AgentState(Dict):
    """Type for agent state."""
    messages: List
    
# Define the graph builder function
@asynccontextmanager
async def graph():
    """
    Create the LangGraph ReAct agent.
    
    Returns:
        A LangGraph runnable that can be used to invoke the agent.
    """
    # Create the agent using our MCP integration
    async with create_mcp_agent() as agent:
        # Wrap the agent in a StateGraph
        workflow = StateGraph(AgentState)
        
        async def run_agent(state: AgentState) -> AgentState:
            """Run the ReAct agent."""
            result = await agent.ainvoke({"messages": state["messages"]})
            return {"messages": result["messages"]}
        
        # Add nodes and edges
        workflow.add_node("agent", run_agent)
        workflow.add_edge("agent", END)
        workflow.set_entry_point("agent")
        
        # Compile the graph
        compiled = workflow.compile()
        yield compiled
