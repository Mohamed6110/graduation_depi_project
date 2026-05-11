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
    HOTEL_PLANNER,
    HOTEL_SEARCHER,
    HOTEL_ADVISOR,
    HOTEL_BOOKING_AGENT,
)



# ============================================================================
# ACTIVITY SUB-AGENTS
# ============================================================================

hotel_planner = create_agent(
    model=llm,
    name="hotel_planner",
    checkpointer=checkpointer,
    system_prompt=HOTEL_PLANNER,
)

hotel_searcher = create_agent(
    model=llm,
    name="hotel_searcher",
    tools=tools_composio + [search_tool],
    checkpointer=checkpointer,
    system_prompt=HOTEL_SEARCHER,
)

hotel_advisor = create_agent(
    model=llm,
    name="hotel_advisor",
    checkpointer=checkpointer,
    system_prompt=HOTEL_ADVISOR,
)

@tool("hotel_planner", description="Create detailed hotel search plans from user requests.")
def ask_hotel_planner(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"planner_{uuid.uuid4()}"}}
    result = hotel_planner.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("hotel_searcher", description="Execute hotel searches using web tools to find actual hotels and accommodations.")
def ask_hotel_searcher(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"searcher_{uuid.uuid4()}"}}
    result = hotel_searcher.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("hotel_advisor", description="Provide personalized hotel recommendations and itinerary guidance.")
def ask_hotel_advisor(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"advisor_{uuid.uuid4()}"}}
    result = hotel_advisor.invoke(
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

hotel_booking = create_agent(
    model=llm,
    tools=[
        ask_hotel_planner,
        ask_hotel_searcher,
        ask_hotel_advisor,   
    ],
    checkpointer=checkpointer,
    system_prompt=HOTEL_BOOKING_AGENT,
)



