# Rehla (AI) 🌍

Rehla (which means "Journey" in Arabic) is a travel assistant built using a multi-agent architecture. It helps with planning trips, booking flights and hotels, finding activities, and managing travel logistics—all through a chat interface. 

The project is built with **LangChain** and **LangGraph**, and it uses several specialized AI agents working together to handle different parts of the travel experience.

---

## What It Does

Instead of relying on a single AI model to do everything, Rehla divides the work among 9 specialized agents:

- 🛫 **Flight Agent:** Searches for and compares flights across different airlines.
- 🏨 **Hotel Agent:** Finds accommodations and manages bookings.
- 🎭 **Activity Agent:** Looks for tours, attractions, and local entertainment.
- 🗺️ **Local Experiences Agent:** Finds hidden gems and authentic cultural spots.
- 🍽️ **Dining Agent:** Recommends restaurants and helps with reservations.
- 🛟 **Support Agent:** Provides navigation, emergency contacts, and language translation.
- 💳 **Booking Agent:** Manages the actual reservations, payments, and cancellations.
- 📋 **Logistics Agent:** Puts everything together into a day-by-day itinerary.
- ⚖️ **Compliance Agent:** Checks visa requirements and travel regulations.

---

## How It Works (Architecture)

The system is designed around a root agent (`REHLA_AGENT`) that takes your prompt, figures out what you need, and hands off the task to the right specialist.

For example, if you ask to book an activity, the root agent passes the request to the **Activity Agent**, which might then break it down further (e.g., using a planner, a searcher, and an advisor sub-agent) before giving you the final answer.

**Tech Stack:**
- **LangChain & LangGraph:** For agent workflow and state management.
- **Composio:** To integrate external tools and APIs.
- **Tavily:** For real-time web search.
- **Ollama:** Runs the LLM locally or via the cloud (default: `gpt-oss:120b-cloud`).

---

## Setup & Installation

### 1. Requirements
Make sure you have Python 3.10+ and `pip` installed. You'll also need [Ollama](https://ollama.com/) running.

### 2. Install Dependencies
Clone the repo and install the required packages:

```bash
git clone <repository-url>
cd graduation_depi_projects/rehla
pip install -r requirements.txt
```
*(If you don't have a requirements.txt, you can install them manually: `pip install langchain langchain-core langgraph composio-langchain tavily-python python-dotenv`)*

### 3. Environment Variables
Create a `.env` file in the `rehla` folder and add your API keys:

```env
# Required
TAVILY_API_KEY=your_tavily_api_key
COMPOSIO_API_KEY=your_composio_api_key

# Optional (for LangSmith tracing)
LANGSMITH_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=rehla_project
```

---

## Running the Project

To start the chat assistant, run:

```bash
cd rehla
python agent.py
```

You can try asking things like:
- *"Plan a 5-day trip to Italy including flights and hotels."*
- *"What are some authentic local experiences in Kyoto?"*
- *"Do I need a visa to travel to Japan from Egypt?"*

Type `exit`, `quit`, or `q` to close the chat.

---

## Project Layout

Here is a quick overview of how the code is organized:

```text
rehla/
├── agent.py                 # The main entry point and root agent
├── config.py                # LLM setup and API keys
├── prompt.py                # System prompts
├── tools.py                 # External integrations (Tavily, Composio)
├── .env                     # Your environment variables
└── [domain]_agent/          # Folders for each specialized agent (flight, hotel, etc.)
    ├── agent.py             # Logic for the specific agent
    └── prompt.py            # Prompts specific to that agent
```

---
*Built as a DEPI Graduation Project.*
