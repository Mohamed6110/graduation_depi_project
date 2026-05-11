from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from composio import Composio
from langchain_mcp_adapters.client import MultiServerMCPClient
from composio_langchain import LangchainProvider
import asyncio
import uuid
from langchain_tavily import TavilyCrawl
from langchain.tools import tool
from config import *
from tools import *
from .prompt import (
    ITINERARY_BUILDER,
    TRANSPORTATION_AGENT,
    REMINDER_AGENT,
    COORDINATION_AGENT,
    LOGISTICS_COORDINATOR
)



# ============================================================================
# ACTIVITY SUB-AGENTS
# ============================================================================

itinerary_builder_agent = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    name="itinerary_builder",
    system_prompt=ITINERARY_BUILDER,
)

transportation_agent = create_agent(
    model=llm,
    tools=tools_composio + [search_tool],
    checkpointer=checkpointer,
    system_prompt=TRANSPORTATION_AGENT,
)

reminder_agent = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    system_prompt=REMINDER_AGENT,
)
coordination_agent = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    system_prompt=COORDINATION_AGENT,
)

@tool("itinerary_builder", description="Create comprehensive travel itineraries with day-by-day planning and optimization.")
def ask_itinerary_builder(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"planner_{uuid.uuid4()}"}}
    result = itinerary_builder_agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("transportation_agent",description="Coordinate comprehensive transportation solutions for entire trips.")
def ask_transportation_agent(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"searcher_{uuid.uuid4()}"}}
    result = transportation_agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("reminder agent",     description="Provide comprehensive travel reminder and notification systems.")
def ask_reminder_agent(query: str) -> str:
    
    config = {"configurable": {"thread_id": f" reminder{uuid.uuid4()}"}}
    result = reminder_agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("coordination_agent",     description="Provide cross-service coordination and trip optimization.")
def ask_coordination_agent(query: str) -> str:
    
    config = {"configurable": {"thread_id": f" coordinator_{uuid.uuid4()}"}}
    result = coordination_agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
# ============================================================================
# MAIN ACTIVITY BOOKING AGENT
# ============================================================================

logistics_coordinator = create_agent(
    model=llm,
    tools=[
        ask_itinerary_builder,
        ask_transportation_agent,
        ask_reminder_agent,
        ask_coordination_agent,   
    ],
    checkpointer=checkpointer,
    system_prompt=LOGISTICS_COORDINATOR,
)

