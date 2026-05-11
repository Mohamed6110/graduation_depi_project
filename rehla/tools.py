from config import *
from langchain.tools import tool

@tool
def search_tool(query: str) -> str:
    """
    Search for current, real-world information on any topic.

    Use this for:
    - Recent developments, news, or updates
    - Verifying facts that may have changed
    

    Do NOT use for timeless concepts (e.g., 'what is a variable') —
    answer those directly from knowledge.

    Args:
        query: A specific, focused search query (3-8 words ideal)
    """
    result = tavily_client.search(query)
    return str(result.get("results", result))

# Initialize Composio with LangChain provider
composio = Composio(provider=LangchainProvider(),api_key=COMPOSIO_API_KEY)
# # session = composio.create(user_id="default")

# # # Get tools from specific toolkits
# # You can specify one or more toolkits
# tools_composio = session.tools()
tools_composio = composio.tools.get(
    user_id="default",
    toolkits=["composio_search","webscraping_ai"]
)