'''
Find dining options in Johns Creek for 3 adults, September 5-12, 2025. Interested in traditional Indian and vegetarian-friendly restaurants. One special birthday dinner, budget $50-200 per person. Need help with reservations.
'''

"""Dining agent and sub-agents, handling restaurant discovery, culinary experiences, and dining reservations."""


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
    RESTAURANT_DISCOVERY,
    RESTAURANT_SEARCHER,
    CUISINE_EXPERIENCE,
    DINING_RESERVATION,
    DINING_COORDINATOR
)



# ============================================================================
# ACTIVITY SUB-AGENTS
# ============================================================================

restaurant_discovery_agent = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    system_prompt=RESTAURANT_DISCOVERY,
)

restaurant_searcher = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=checkpointer,
    system_prompt=RESTAURANT_SEARCHER,
)

cuisine_experience_agent = create_agent(
    model=llm,
    
    checkpointer=checkpointer,
    system_prompt=CUISINE_EXPERIENCE,
)
dining_reservation_agent = create_agent(
    model=llm,
    
    checkpointer=checkpointer,
    system_prompt=DINING_RESERVATION,
)

@tool("cuisine_experience_agent", description="Create detailed restaurant search plans from user dining requests.")
def ask_restaurant_discovery_agent(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"experience_{uuid.uuid4()}"}}
    result = restaurant_discovery_agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("cuisine_experience_agent", description="Provide personalized cuisine experience recommendations.")
def ask_cuisine_experience_agent(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"experience_{uuid.uuid4()}"}}
    result = cuisine_experience_agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("restaurant_searcher", description="Execute restaurant searches using web tools to find actual restaurants and dining experiences.")
def ask_restaurant_searcher(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"searcher_{uuid.uuid4()}"}}
    result = restaurant_searcher.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("dining_reservation_agent", description="Provide restaurant booking guidance and reservation coordination.")
def ask_dining_reservation_agent(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"reservation_{uuid.uuid4()}"}}
    result = dining_reservation_agent.invoke(
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

dining_coordination = create_agent(
    model=llm,
    tools=[ask_restaurant_discovery_agent ,
        ask_cuisine_experience_agent,
        ask_restaurant_searcher,
        ask_dining_reservation_agent, 
         
    ],
    checkpointer=checkpointer,
    system_prompt=DINING_COORDINATOR,
)



