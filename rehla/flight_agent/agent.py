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
    FLIGHT_PLANNER,
    FLIGHT_SEARCHER,
    FLIGHT_ADVISOR,
    FLIGHT_BOOKING_AGENT
)




# ============================================================================
# ACTIVITY SUB-AGENTS
# ============================================================================

flight_planner = create_agent(
    model=llm,
    name="flight_planner",
    checkpointer=checkpointer,
    system_prompt=FLIGHT_PLANNER,
)

flight_searcher = create_agent(
    model=llm,
    tools=tools_composio + [search_tool],
    checkpointer=checkpointer,
    name="flight_searcher",
    system_prompt=FLIGHT_SEARCHER,
)

flight_advisor = create_agent(
    model=llm,
    checkpointer=checkpointer,
    name="flight_advisor",
    system_prompt=FLIGHT_ADVISOR,
)

@tool("flight_planner", description="Create detailed flight search plans from user requests.")
def ask_flight_planner(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"planner_{uuid.uuid4()}"}}
    result = flight_planner.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("flight_searcher", description="Execute flight searches using web tools to find actual flights and travel options.")
def ask_flight_searcher(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"searcher_{uuid.uuid4()}"}}
    result = flight_searcher.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("flight_advisor", description="Provide personalized flight recommendations and itinerary guidance.")
def ask_flight_advisor(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"advisor_{uuid.uuid4()}"}}
    result = flight_advisor.invoke(
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

flight_booking = create_agent(
    model=llm,
    tools=[
        ask_flight_planner,
        ask_flight_searcher,
        ask_flight_advisor,   
    ],
    checkpointer=checkpointer,
    system_prompt=FLIGHT_BOOKING_AGENT,
)



