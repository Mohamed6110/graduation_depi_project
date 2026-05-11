"""Booking coordinator agent and sub-agents, handling payment processing, confirmations, and booking management."""



from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from composio import Composio
from composio_langchain import LangchainProvider
import asyncio
import uuid
from langchain.tools import tool
from config import *
from tools import *

from .prompt import (
    PAYMENT_PROCESSING,
    CONFIRMATION_AGENT,
    MODIFICATION_AGENT,
    BOOKING_COORDINATOR
)



# ── Shared LLM ────────────────────────────────────────────────────────────────






# ============================================================================
# ACTIVITY SUB-AGENTS
# ============================================================================
payment_processing_agent= create_agent(
    model=llm,
    checkpointer=checkpointer,
    system_prompt=PAYMENT_PROCESSING,
)

confirmation_agent = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    system_prompt=CONFIRMATION_AGENT,
)

modification_agent = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    system_prompt=MODIFICATION_AGENT,
)

@tool("payment_processor",description="Provide mock payment processing demonstrations and security education.",
)
def ask_payment_processor(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"processor_{uuid.uuid4()}"}}
    result = payment_processing_agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("confirmation_agent",    description="Provide booking confirmation management and verification assistance.")
def ask_confirmation_agent(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"confirmation_{uuid.uuid4()}"}}
    result = confirmation_agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("modification_agent",description="Provide booking modification, cancellation, and change management assistance.",
)
def ask_modification_agent(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"modification_{uuid.uuid4()}"}}
    result = modification_agent.invoke(
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

booking_coordinator = create_agent(
    model=llm,
    tools=[
        ask_payment_processor,
        ask_confirmation_agent,
        ask_modification_agent,
    ],
    checkpointer=checkpointer,
    system_prompt=BOOKING_COORDINATOR,
)



