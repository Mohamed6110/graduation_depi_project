"""Centralized configuration for AI Wanderize travel system."""
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from composio import Composio
from langchain_mcp_adapters.client import MultiServerMCPClient
from composio_langchain import LangchainProvider
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv()
import os
# Initialize Composio
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "teacher"
os.environ.get("LANGSMITH_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
COMPOSIO_API_KEY = os.environ.get("COMPOSIO_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

llm= init_chat_model(model="ollama:gpt-oss:120b-cloud ", temperature=0.0)

checkpointer = InMemorySaver()