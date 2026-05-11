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
    NAVIGATION_AGENT,
    EMERGENCY_SUPPORT,
    LOCAL_ASSISTANCE,
    LANGUAGE_SUPPORT,
    SUPPORT_COORDINATOR
)




# ============================================================================
# ACTIVITY SUB-AGENTS
# ============================================================================

navigation_agent = create_agent(
    model=llm,
    tools=[search_tool],
    name="navigation_agent",
    checkpointer=checkpointer,
    system_prompt=NAVIGATION_AGENT,
)

emergency_support = create_agent(
    model=llm,
    tools=[search_tool],
    name="emergency_support",
    checkpointer=checkpointer,
    system_prompt=EMERGENCY_SUPPORT,
)

local_assistance = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    name="local_assistance",
    system_prompt=LOCAL_ASSISTANCE,
)
language_support_agent = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    name="language_support_agent",
    system_prompt=LANGUAGE_SUPPORT,
)

@tool("navigation_agent", description="Provide real-time navigation assistance and routing guidance.")
def ask_navigation_agent(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"planner_{uuid.uuid4()}"}}
    result = navigation_agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("emergency_support",description="Provide 24/7 emergency assistance and crisis support for travelers.")
def ask_emergency_support(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"emergency_{uuid.uuid4()}"}}
    result = emergency_support.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("local_assistance",description="Provide on-ground local support and practical travel assistance.")
def ask_local_assistance(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"local_assistance_{uuid.uuid4()}"}}
    result = local_assistance.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("language_support_agent",description="Provide translation assistance and communication support.")
def ask_language_support_agent(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"language_support_agent_{uuid.uuid4()}"}}
    result = language_support_agent.invoke(
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

support_coordinator= create_agent(
    model=llm,
    tools=[
        ask_navigation_agent,
        ask_emergency_support,
        ask_local_assistance,
        ask_language_support_agent
    ],
    checkpointer=checkpointer,
    system_prompt=SUPPORT_COORDINATOR,
)

