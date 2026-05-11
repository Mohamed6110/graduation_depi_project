"""Activity booking agent and sub-agents, handling activity search, planning, and advisory."""


from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from composio import Composio
from langchain_mcp_adapters.client import MultiServerMCPClient
from composio_langchain import LangchainProvider
import asyncio
import uuid
from langchain.tools import tool
from config import *
from tools import *


from .prompt import (
    ACTIVITY_PLANNER,
    ACTIVITY_SEARCHER,
    ACTIVITY_ADVISOR,
    ACTIVITY_BOOKING_AGENT,
)



# ── Shared LLM ────────────────────────────────────────────────────────────────






# ============================================================================
# ACTIVITY SUB-AGENTS
# ============================================================================

activity_planner = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    system_prompt=ACTIVITY_PLANNER,
)

activity_searcher = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    system_prompt=ACTIVITY_SEARCHER,
)

activity_advisor = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    system_prompt=ACTIVITY_ADVISOR,
)

@tool("activity_planner", description="Create detailed activity search plans from user requests.")
def ask_activity_planner(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"planner_{uuid.uuid4()}"}}
    result = activity_planner.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("activity_searcher", description="Execute activity searches using web tools to find actual activities and experiences.")
def ask_activity_searcher(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"searcher_{uuid.uuid4()}"}}
    result = activity_searcher.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("activity_advisor", description="Provide personalized activity recommendations and itinerary guidance.")
def ask_activity_advisor(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"advisor_{uuid.uuid4()}"}}
    result = activity_advisor.invoke(
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

activity_booking = create_agent(
    model=llm,
    tools=[
        ask_activity_planner,
        ask_activity_searcher,
        ask_activity_advisor,   
    ],
    checkpointer=checkpointer,
    system_prompt=ACTIVITY_BOOKING_AGENT,
)

