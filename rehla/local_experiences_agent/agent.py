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
    LOCAL_PLANNER,
    LOCAL_SEARCHER,
    LOCAL_ADVISOR,
    LOCAL_BOOKING_AGENT,
)



# ============================================================================
# ACTIVITY SUB-AGENTS
# ============================================================================

local_planner = create_agent(
    model=llm,
    name="local_planner",
    checkpointer=checkpointer,
    system_prompt=LOCAL_PLANNER,
)

local_searcher = create_agent(
    model=llm,
    tools=tools_composio + [search_tool],
    name="local_searcher",
    checkpointer=checkpointer,
    system_prompt=LOCAL_SEARCHER,
)

local_advisor = create_agent(
    model=llm,
    name="local_advisor",
    checkpointer=checkpointer,
    system_prompt=LOCAL_ADVISOR,
)

@tool("local_planner",description="Create detailed authentic local experience search plans from user requests.",
)
def ask_local_planner(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"planner_{uuid.uuid4()}"}}
    result = local_planner.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("local_searcher", description="Execute searches for authentic local experiences, hidden gems, and cultural immersion opportunities.")
def ask_local_searcher(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"searcher_{uuid.uuid4()}"}}
    result = local_searcher.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("local_advisor", description="Provide authentic local experience recommendations and cultural immersion guidance.")
def ask_local_advisor(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"advisor_{uuid.uuid4()}"}}
    result = local_advisor.invoke(
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

local_experiences = create_agent(
    model=llm,
    tools=[
        ask_local_planner,
        ask_local_searcher,
        ask_local_advisor,   
    ],
    checkpointer=checkpointer,
    # description="Complete local experiences coordination handling authentic discovery, cultural immersion planning, and community connections.",
    system_prompt=LOCAL_BOOKING_AGENT,
)



