# Rehla (رحلة) — AI Travel Assistant 🌍✈️

> **Rehla** means *"Journey"* in Arabic. It's not just a travel app — it's your personal AI travel team, available 24/7.

Rehla is an intelligent travel assistant built on a **multi-agent architecture**, designed to handle every aspect of your trip — from the first search to the final day of your journey. Instead of a single AI trying to do everything, Rehla deploys **9 specialized agents**, each an expert in its domain, all working together seamlessly through a clean **Streamlit chat interface**.

---

## ✨ Why Rehla?

Most travel apps make you jump between 5 different websites to plan a single trip. Rehla brings everything into one conversation. Ask it anything — it figures out which expert to call, gets the answer, and delivers it back to you — all in real time.

---

## 🤖 The Agent Team

| Agent | Role |
|---|---|
| 🛫 **Flight Agent** | Searches and compares flights across airlines and dates |
| 🏨 **Hotel Agent** | Finds accommodations and manages booking requests |
| 🎭 **Activity Agent** | Discovers tours, attractions, and local entertainment |
| 🗺️ **Local Experiences Agent** | Uncovers hidden gems and authentic cultural spots |
| 🍽️ **Dining Agent** | Recommends restaurants and handles reservations |
| 🛟 **Support Agent** | Navigation help, emergency contacts, and live translation |
| 💳 **Booking Agent** | Manages reservations, payments, and cancellations |
| 📋 **Logistics Agent** | Assembles everything into a day-by-day itinerary |
| ⚖️ **Compliance Agent** | Checks visa requirements and travel regulations |

---

## 🏗️ Architecture

Rehla is built around a **root orchestrator** (`REHLA_AGENT`) that receives your message, understands your intent, and routes the task to the right specialist agent — or a combination of them.

```
User Message
     ↓
REHLA_AGENT (Orchestrator)
     ├── Flight Agent       → sub-agents: searcher, comparator
     ├── Hotel Agent        → sub-agents: finder, advisor
     ├── Activity Agent     → sub-agents: planner, searcher, advisor
     ├── Dining Agent       → sub-agents: recommender, booker
     ├── Logistics Agent    → assembles full itinerary
     ├── Compliance Agent   → visa & regulation checks
     └── ...
          ↓
    Synthesized Response → Streamlit UI (streamed character by character)
```

Each specialized agent can further break down its task into sub-agents — making the system **deeply capable** without overwhelming any single model.

---

## 🖥️ Streamlit UI

Rehla features a fully interactive chat interface built with **Streamlit**:

- 💬 **Real-time streaming** — responses appear character by character
- 🗂️ **Multi-session support** — manage multiple trip plans simultaneously
- 🧠 **Persistent memory** — each session remembers your full conversation
- 🌙 **Dark mode design** — clean, modern, travel-themed interface
- 📱 **Responsive layout** — works on desktop and mobile browsers

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **LangChain & LangGraph** | Agent workflow, state management, and routing |
| **Streamlit** | Chat UI with real-time streaming |
| **Composio** | External tool integrations (booking APIs, calendars) |
| **Tavily** | Real-time web search for flights, hotels, and activities |
| **Ollama** | Local or cloud LLM inference (`gpt-oss:120b-cloud`) |
| **LangSmith** | Full agent tracing and observability |
| **python-dotenv** | Secure environment variable management |

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running
- API keys for Tavily and Composio

### 1. Clone the Repository

```bash
git clone <repository-url>
cd graduation_depi_projects/rehla
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install langchain langchain-core langgraph composio-langchain tavily-python python-dotenv streamlit
```

### 3. Configure Environment Variables

Create a `.env` file in the `rehla/` folder:

```env
# ── Required ──
TAVILY_API_KEY=your_tavily_api_key
COMPOSIO_API_KEY=your_composio_api_key

# ── Streamlit (optional) ──
STREAMLIT_SERVER_PORT=8501

# ── LangSmith Tracing (optional but recommended) ──
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=rehla_project
```

---

## 🚀 Running the Project

### Chat UI (Streamlit) — Recommended

```bash
cd rehla
streamlit run app.py
```

Then open your browser at `http://localhost:8501`

### Terminal Mode

```bash
cd rehla
python agent.py
```

---

## 💬 Example Prompts

```
"Plan a 5-day trip to Italy including flights and hotels from Cairo."
"What are some authentic local experiences in Kyoto, Japan?"
"Do I need a visa to travel to Japan from Egypt?"
"Find me a good seafood restaurant near the Eiffel Tower."
"Book the cheapest flight from Cairo to Dubai next Friday."
"What's the weather like in Istanbul in December?"
"Create a day-by-day itinerary for 7 days in Spain."
```

---

## 📁 Project Structure

```
rehla/
├── app.py                      # Streamlit UI — main entry point
├── agent.py                    # Root orchestrator (REHLA_AGENT)
├── config.py                   # LLM setup and API key loading
├── prompt.py                   # Root agent system prompt
├── tools.py                    # Tavily search + Composio integrations
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not committed)
│
├── flight_agent/
│   ├── agent.py                # Flight search and comparison logic
│   └── prompt.py               # Flight agent system prompt
│
├── hotel_agent/
│   ├── agent.py                # Hotel search and booking logic
│   └── prompt.py               # Hotel agent system prompt
│
├── activity_agent/
│   ├── agent.py                # Activity discovery logic
│   └── prompt.py               # Activity agent system prompt
│
├── dining_agent/
│   ├── agent.py                # Restaurant recommendations
│   └── prompt.py               # Dining agent system prompt
│
├── logistics_agent/
│   ├── agent.py                # Itinerary assembly logic
│   └── prompt.py               # Logistics agent system prompt
│
├── compliance_agent/
│   ├── agent.py                # Visa and regulation checks
│   └── prompt.py               # Compliance agent system prompt
│
├── booking_agent/
│   ├── agent.py                # Reservation management
│   └── prompt.py               # Booking agent system prompt
│
├── support_agent/
│   ├── agent.py                # Navigation, translation, emergency
│   └── prompt.py               # Support agent system prompt
│
└── local_experiences_agent/
    ├── agent.py                # Hidden gems and cultural spots
    └── prompt.py               # Local experiences agent system prompt
```

---

## 🔑 Getting API Keys

| Service | Link | Free Tier |
|---|---|---|
| Tavily | [app.tavily.com](https://app.tavily.com) | ✅ 1000 searches/month |
| Composio | [composio.dev](https://composio.dev) | ✅ Free tier available |
| LangSmith | [smith.langchain.com](https://smith.langchain.com) | ✅ Free |
| Ollama | [ollama.com](https://ollama.com) | ✅ Fully free (local) |

---

## 🗺️ Roadmap

- [ ] Payment integration via Composio (Simulation)
- [ ] Real booking API connections (Skyscanner, Booking.com)
- [ ] Multi-language support (Arabic, French, Spanish)


---

## 👥 Team

Built as a **DEPI Graduation Project** — demonstrating production-grade multi-agent AI systems applied to real-world travel use cases.

---

*Powered by LangGraph · LangChain · Streamlit · Composio · Tavily · Ollama*
