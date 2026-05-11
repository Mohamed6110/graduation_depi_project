from __future__ import annotations

import logging
import operator
from enum import Enum
from typing import Annotated, Any, Literal, Sequence, TypedDict
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
import uuid
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Send
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from activity_agent.agent import activity_booking
from booking_agent.agent import booking_coordinator
from dining_agent.agent import dining_coordination
from flight_agent.agent import flight_booking
from hotel_agent.agent import hotel_booking
from local_experiences_agent.agent import local_experiences
from logistics_agent.agent import logistics_coordinator
from support_agent.agent import support_coordinator
from compliance_agent.agent import agent as compliance_agent
from prompt import TRAVEL_ASSISTANT
from config import *
from tools import *


# ── Sub-agent tools ────────────────────────────────────────────────────────────
# Each sub-agent is wrapped as a callable tool so the root agent can delegate.

@tool("activity_booking", description="Complete activity booking coordination handling planning, searching, and advisory services.")
def ask_activity_booking(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"booking_{uuid.uuid4()}"}}
    result = activity_booking.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("booking_coordinator", description="Complete booking coordination handling payment processing, confirmations, and modifications.")
def ask_booking_coordinator(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"coordinator_{uuid.uuid4()}"}}
    result = booking_coordinator.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("dining_coordination",description="Complete dining coordination handling restaurant discovery, culinary experiences, and reservation management.")
def ask_dining_coordination(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"coordination_{uuid.uuid4()}"}}
    result = dining_coordination.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""

@tool("flight_booking",description="Complete flight booking coordination handling planning, searching, and advisory services.")
def ask_flight_booking(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"booking_{uuid.uuid4()}"}}
    result = flight_booking.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("hotel_booking",description="Complete hotel booking coordination handling planning, searching, and advisory services.")
def ask_hotel_booking(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"booking_{uuid.uuid4()}"}}
    result = hotel_booking.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("local_experiences",description="Complete local experiences coordination handling authentic discovery, cultural immersion planning, and community connections.")
def ask_local_experiences(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"experiences_{uuid.uuid4()}"}}
    result = local_experiences.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("logistics_coordinator",description="Complete logistics coordination handling itinerary creation, transportation planning, reminder systems, and cross-service coordination.")
def ask_logistics_coordinator(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"coordinator_{uuid.uuid4()}"}}
    result = logistics_coordinator.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("support_coordinator",description="Complete travel support coordination handling navigation, emergency assistance, local support, and language help.")
def ask_support_coordinator(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"coordinator_{uuid.uuid4()}"}}
    result = support_coordinator.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""
@tool("compliance_agent",description="Complete compliance coordination handling travel regulations, legal requirements, and policy adherence.")
def ask_compliance_agent(query: str) -> str:
    
    config = {"configurable": {"thread_id": f"coordinator_{uuid.uuid4()}"}}
    result = compliance_agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                return msg.content
    return ""


TOOLS = [
    ask_activity_booking,
    ask_booking_coordinator,
    ask_dining_coordination,
    ask_flight_booking,
    ask_hotel_booking,
    ask_local_experiences,
    ask_logistics_coordinator,
    ask_support_coordinator,
    ask_compliance_agent
    
]


# ── Root agent ─────────────────────────────────────────────────────────────────

root_agent = create_agent(
    model=llm,
    tools=TOOLS,
    name="REHLA_AGENT",
    system_prompt=TRAVEL_ASSISTANT,
    checkpointer=InMemorySaver(),
)
config = {"configurable": {"thread_id": "travel_chat_1"}}

print("--- travel Agent Chat (Type 'exit' to stop) ---")
import sys
import time

def run():
    while True:
        user_input = input("User: ")
        print("user: ",user_input)
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Chat ended.")
            break

        inputs = {"messages": [("user", user_input)]}

        # Keep track of the message content
        final_text = ""

        for chunk in root_agent.stream(
            inputs, config=config, stream_mode="values"
        ):
            final_message = chunk["messages"][-1]
            # Convert to string if it's not already
            content = final_message.content
            if isinstance(content, list):
                # Handle list of content blocks
                final_text = "".join(
                    block.get("text", str(block)) if isinstance(block, dict) else str(block)
                    for block in content
                )
            else:
                final_text = str(content)

        # Custom typewriter output
        print("Assistant: ", end="", flush=True)
        for char in final_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.02)  # Adjust speed here (lower = faster)
        
        print("\n")

if __name__ == "__main__":
    run()
